#coding:utf-8
#-----------------------------
#code by Chenlin 2017-03-18 10:36:21
#功能:依照DataStruct_intrap结构体对参数检查后的结构数据*_ConvertedData进行解析,提取出感兴趣的信息.
#displaydata -datatinfo  datapath callname  :获取callname的结构信息
#displaydata -datatinfo -a  datapath :获取所有函数的结构信息
#displaydata -checkinfo datapath callname :获取callname的检查信息及其比例统计
#displaydata -checkinfo -a datapath :获取所有函数的检查信息及其比例统计
#displaydata -checkedcall datapath ratio:获取比率为ratio设置下,参数检查的callname
#displaydata -checkstat datapath :获取各类参数检查的统计信息
#-----------------------------

import sys
sys.path.append("..")
import commonFile.DataStruct as DataStruct
import commonFile.DataStruct_D as DataStruct_D
import commonFile.DataStruct_M as DataStruct_M
import commonFile.OPS_DataStruct as OPS_DataStruct
from commonFile.ObjDataAndBinFile import ObjDataAndBinFile


class displaydata:
    def run(self,cmd):
        #print cmd
        if len(cmd)==4 and cmd.__contains__("-datainfo") and (not cmd.__contains__("-a")):
            self.GetDatainfo_Call(cmd)
            return
        elif len(cmd)==4 and cmd.__contains__("-datainfo") and cmd.__contains__("-a"):
            self.GetDatainfo_AllCall(cmd)
            return
        elif len(cmd)==4 and cmd.__contains__("-checkinfo") and (not cmd.__contains__("-a")):
            self.GetCheckinfo_Call(cmd)
            return
        elif len(cmd)==4 and cmd.__contains__("-uncheckinfo") and (not cmd.__contains__("-a")):
            self.GetUnCheckinfo_Call(cmd)
            return
        elif len(cmd)==4 and cmd.__contains__("-checkinfo") and cmd.__contains__("-a"):
            self.GetCheckinfo_AllCall(cmd)
            return
        elif len(cmd)==4 and cmd.__contains__("-uncheckinfo") and cmd.__contains__("-a"):
            self.GetUnCheckinfo_AllCall(cmd)
            return
        elif len(cmd)==4 and cmd.__contains__("-checkedcall"):
            self.GetCheckedCall(cmd)
            return
        elif len(cmd)==5 and cmd.__contains__("-checkedcall2"):
            self.GetCheckedCall2(cmd)
            return
        elif len(cmd)==3 and cmd.__contains__("-checkstat"):
            self.GetCheckedStat(cmd)
            return
        else:
            print "\n#功能: 依照DataStruct_intrap结构体对参数检查后的结构数据*_ConvertedData进行解析,提取相关信息."
            print "\n#用法:  displaydata -datainfo  datapath callname  :获取callname的结构信息"
            print "\tdisplaydata -datainfo -a  datapath :获取所有函数的结构信息"
            print "\n\tdisplaydata -checkinfo datapath callname :获取callname的检查信息及其比例统计"
            print "\n\tdisplaydata -uncheckinfo datapath callname :获取callname的未检查信息及其比例统计"
            print "\tdisplaydata -checkinfo -a datapath :获取所有函数的检查信息及其比例统计"
            print "\n\tdisplaydata -checkedcall datapath ratio:获取比率为ratio设置下,参数检查的callname [有诸多变形]\n"
            print "\n\tdisplaydata -checkedcall2 datapath ratio_1 ratio_2:获取比率为[ratio_1,ratio_2]设置下,参数检查的callname [有诸多变形]\n"
            print "\n\tdisplaydata -checkstat datapath :获取各类参数检查的统计信息\n"
        return
    #displaydata -datatinfo  datapath callname  :获取callname的结构信息"
    def GetDatainfo_Call(self,cmd):
        datapath = cmd[2]
        callname = cmd[3]
        print "%s 的结构信息:"%callname
        dbcalls = self.LoadData(datapath)
        for call in dbcalls.callinfolist:
            if(call.call_code == callname):
                self.printdatainfo(call)
                break
        return

    def GetDatainfo_AllCall(self,cmd):
        datapath = cmd[3]
        print "代码库中所有函数的结构信息:"
        dbcalls = self.LoadData(datapath)
        self.printdatainfo(dbcalls.callinfolist)
        return

    def GetCheckinfo_Call(self,cmd):
        datapath = cmd[2]
        callname = cmd[3]
        print "%s 的检查信息:"%callname
        dbcalls = self.LoadData(datapath)
        for call in dbcalls.callinfolist:
            if(call.call_code == callname):
                self.printcheckinfo(call)
                break
        return
    def GetUnCheckinfo_Call(self,cmd):
        datapath = cmd[2]
        callname = cmd[3]
        print "%s 的未检查信息:"%callname
        dbcalls = self.LoadData(datapath)
        for call in dbcalls.callinfolist:
            if(call.call_code == callname):
                self.printuncheckinfo(call)
                break
        return

    def GetCheckinfo_AllCall(self,cmd):
        datapath = cmd[3]
        print "代码库中所有函数的检查信息:"
        dbcalls = self.LoadData(datapath)
        self.printcheckinfo(dbcalls.callinfolist)
        return

    def GetUnCheckinfo_AllCall(self,cmd):
        datapath = cmd[3]
        print "代码库中所有函数的检查信息:"
        dbcalls = self.LoadData(datapath)
        self.printuncheckinfo(dbcalls.callinfolist)
        return

    def GetCheckedCall(self,cmd):
        datapath = cmd[2]
        ratio = cmd[3]
        dbcalls = self.LoadData(datapath)
        self.getcheckedcall_new(dbcalls.callinfolist,ratio)
        return

    def GetCheckedCall2(self,cmd):
        datapath = cmd[2]
        ratio_1 = cmd[3]
        ratio_2 = cmd[4]
        dbcalls = self.LoadData(datapath)
        self.getcheckedcall_r1_r2(dbcalls.callinfolist,ratio_1,ratio_2)
        return

    def GetCheckedStat(self,cmd):
        datapath = cmd[2]
        dbcalls = self.LoadData(datapath)
        self.getcheckstatistic(dbcalls.callinfolist)
        return
    def getcheckedcall(self,call,ratio):
        ratio = float(ratio)
        #print 1-(int)ratio
        num_callsite =0
        num_scheck_ctr = 0
        num_scheck_noctr = 0
        num_mcheck_def = 0
        num_mcheck_ctr = 0
        num_mcheck_noctr = 0
        num_nocheck =0
        num_checkcall =0
        num_errcall=0
        if(type(call) == list):
            for atomcall in call:
                s_out = ""
                i=0
                num_callsite = len(atomcall.callsiteinfolist)
                if(num_callsite == 0):
                    num_errcall += 1
                    # 输出包含错误数据的函数(callsiteNums =0)
                    #print "**********\n%d: %s callsiteNums=%s, call_id=%d\n**********"%(num_errcall,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id)
                    continue

                num_scheck_ctr = 0
                num_scheck_noctr = 0
                num_mcheck_def = 0
                num_mcheck_ctr = 0
                num_mcheck_noctr = 0
                num_nocheck =0
                for callsite in atomcall.callsiteinfolist:
                    if(callsite.argcheckresult == "单参数检查-控制依赖"):
                        num_scheck_ctr += 1
                    if(callsite.argcheckresult == "单参数检查-非控制条件"):
                        num_scheck_noctr += 1
                    if(callsite.argcheckresult == "联合检查-相互定义"):
                        num_mcheck_def += 1
                    if(callsite.argcheckresult == "联合检查-控制依赖"):
                        num_mcheck_ctr += 1
                    if(callsite.argcheckresult == "联合检查-非控制条件"):
                        num_mcheck_noctr += 1
                    if(callsite.argcheckresult == "无检查"):
                        num_nocheck += 1
                '''
                # 输出满足比率所有对参数进行检查的函数统计信息
                r = 1-float(num_nocheck)/num_callsite
                if r >= ratio:
                    s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
            print "\nALL(%.2f<=r): 参数检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            '''

                # 输出满足比率所有对参数进行检查的函数统计信息,去除为1的call
                r = 1-float(num_nocheck)/num_callsite
                if r >= ratio and r<1.0:
                    s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
            print "\nALL(%.2f<=r<1.0): 参数检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)

            """
                # 输出满足比率所有对参数进行联合检查的函数统计信息
                r = float(num_mcheck_def + num_mcheck_ctr + num_mcheck_noctr)/num_callsite
                if r >= ratio:
                    s_out += "联合检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out

            print "\nALL(%.2f<=r: 联合检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            """

            """
                # 输出满足比率所有对参数进行联合检查的函数统计信息,并去除比率=1的函数,关注异常的函数调用
                r = float(num_mcheck_def + num_mcheck_ctr + num_mcheck_noctr)/num_callsite
                if r >= ratio and r<1.0:
                    s_out += "联合检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
            print "\nALL(%.2f<=r<1.0)): 联合检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            """

                #else:
                    #s_out += "无检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
        else:
            s_out = ""
            i=0
            num_callsite = len(call.callsiteinfolist)
            num_scheck_ctr = 0
            num_scheck_noctr = 0
            num_mcheck_def = 0
            num_mcheck_ctr = 0
            num_mcheck_noctr = 0
            num_nocheck =0
            for callsite in call.callsiteinfolist:
                if(callsite.argcheckresult == "单参数检查-控制依赖"):
                    num_scheck_ctr += 1
                if(callsite.argcheckresult == "单参数检查-非控制条件"):
                    num_scheck_noctr += 1
                if(callsite.argcheckresult == "联合检查-相互定义"):
                    num_mcheck_def += 1
                if(callsite.argcheckresult == "联合检查-控制依赖"):
                    num_mcheck_ctr += 1
                if(callsite.argcheckresult == "联合检查-非控制条件"):
                    num_mcheck_noctr += 1
                if(callsite.argcheckresult == "无检查"):
                    num_nocheck += 1
            r = 1-float(num_nocheck)/num_callsite
            if r >= ratio:
                s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,call.call_code,call.callsiteNums,call.call_id )
                print s_out
            #else:
                #s_out += "无检查(%.2f) %s[%s] : ID = %s  "%(r,call.call_code,call.callsiteNums,call.call_id )


    def getcheckedcall_new(self,call,ratio):
        ratio = float(ratio)
        #print 1-(int)ratio
        num_callsite =0
        num_scheck_ctr = 0
        num_scheck_noctr = 0
        num_mcheck_def = 0
        num_mcheck_ctr = 0
        num_mcheck_noctr = 0
        num_nocheck =0
        num_checkcall =0
        num_errcall=0
        if(type(call) == list):
            for atomcall in call:
                s_out = ""
                i=0
                num_callsite = len(atomcall.callsiteinfolist)
                if(num_callsite == 0):
                    num_errcall += 1
                    # 输出包含错误数据的函数(callsiteNums =0)
                    #print "**********\n%d: %s callsiteNums=%s, call_id=%d\n**********"%(num_errcall,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id)
                    continue

                num_scheck_ctr = 0
                num_scheck_noctr = 0
                num_mcheck_def = 0
                num_mcheck_ctr = 0
                num_mcheck_noctr = 0
                num_nocheck =0
                for callsite in atomcall.callsiteinfolist:
                    if len(callsite.argcheckresult)==0:
                        num_nocheck += 1
                '''
                # 输出满足比率所有对参数进行检查的函数统计信息
                r = 1-float(num_nocheck)/num_callsite
                if r >= ratio:
                    s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
            print "\nALL(%.2f<=r): 参数检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            '''

                # 输出满足比率所有对参数进行检查的函数统计信息,去除为1的call
                r = 1-float(num_nocheck)/num_callsite
                if r >= ratio and r<1.0:
                    s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
                    self.printcheckinfo(atomcall)
            print "\nALL(%.2f<=r<1.0): 参数检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)

            """
                # 输出满足比率所有对参数进行联合检查的函数统计信息
                r = float(num_mcheck_def + num_mcheck_ctr + num_mcheck_noctr)/num_callsite
                if r >= ratio:
                    s_out += "联合检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out

            print "\nALL(%.2f<=r: 联合检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            """

            """
                # 输出满足比率所有对参数进行联合检查的函数统计信息,并去除比率=1的函数,关注异常的函数调用
                r = float(num_mcheck_def + num_mcheck_ctr + num_mcheck_noctr)/num_callsite
                if r >= ratio and r<1.0:
                    s_out += "联合检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
            print "\nALL(%.2f<=r<1.0)): 联合检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            """

                #else:
                    #s_out += "无检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
        else:
            s_out = ""
            i=0
            num_callsite = len(call.callsiteinfolist)
            num_scheck_ctr = 0
            num_scheck_noctr = 0
            num_mcheck_def = 0
            num_mcheck_ctr = 0
            num_mcheck_noctr = 0
            num_nocheck =0
            for callsite in call.callsiteinfolist:
                if len(callsite.argcheckresult) == 0:
                    num_nocheck += 1
            r = 1-float(num_nocheck)/num_callsite
            if r >= ratio:
                s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,call.call_code,call.callsiteNums,call.call_id )
                print s_out
            #else:
                #s_out += "无检查(%.2f) %s[%s] : ID = %s  "%(r,call.call_code,call.callsiteNums,call.call_id )

    def getcheckedcall_r1_r2(self,call,ratio_1,ratio_2):
        r_1 = float(ratio_1)
        r_2 = float(ratio_2)

        #print 1-(int)ratio
        num_callsite =0
        num_scheck_ctr = 0
        num_scheck_noctr = 0
        num_mcheck_def = 0
        num_mcheck_ctr = 0
        num_mcheck_noctr = 0
        num_nocheck =0
        num_checkcall =0
        num_errcall=0
        if(type(call) == list):
            for atomcall in call:
                s_out = ""
                i=0
                num_callsite = len(atomcall.callsiteinfolist)
                if(num_callsite == 0):
                    num_errcall += 1
                    # 输出包含错误数据的函数(callsiteNums =0)
                    #print "**********\n%d: %s callsiteNums=%s, call_id=%d\n**********"%(num_errcall,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id)
                    continue

                num_scheck_ctr = 0
                num_scheck_noctr = 0
                num_mcheck_def = 0
                num_mcheck_ctr = 0
                num_mcheck_noctr = 0
                num_nocheck =0
                for callsite in atomcall.callsiteinfolist:
                    if len(callsite.argcheckresult)==0:
                        num_nocheck += 1
                '''
                # 输出满足比率所有对参数进行检查的函数统计信息
                r = 1-float(num_nocheck)/num_callsite
                if r >= ratio:
                    s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
            print "\nALL(%.2f<=r): 参数检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            '''

                # 输出满足比率所有对参数进行检查的函数统计信息,去除为1的call
                r = 1-float(num_nocheck)/num_callsite
                if r >= r_1 and r<=r_2:
                    s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
                    self.printcheckinfo(atomcall)
            print "\nALL(%.2f<=r<=%.2f): 参数检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(r_1,r_2, num_checkcall,len(call),num_errcall)

            """
                # 输出满足比率所有对参数进行联合检查的函数统计信息
                r = float(num_mcheck_def + num_mcheck_ctr + num_mcheck_noctr)/num_callsite
                if r >= ratio:
                    s_out += "联合检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out

            print "\nALL(%.2f<=r: 联合检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            """

            """
                # 输出满足比率所有对参数进行联合检查的函数统计信息,并去除比率=1的函数,关注异常的函数调用
                r = float(num_mcheck_def + num_mcheck_ctr + num_mcheck_noctr)/num_callsite
                if r >= ratio and r<1.0:
                    s_out += "联合检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                    num_checkcall += 1
                    print s_out
            print "\nALL(%.2f<=r<1.0)): 联合检查的函数数量 = %d 总函数数量 = %d 错误函数数量 = %d"%(ratio, num_checkcall,len(call),num_errcall)
            """

                #else:
                    #s_out += "无检查(%.2f) %s[%s] : ID = %s  "%(r,atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
        else:
            s_out = ""
            i=0
            num_callsite = len(call.callsiteinfolist)
            num_scheck_ctr = 0
            num_scheck_noctr = 0
            num_mcheck_def = 0
            num_mcheck_ctr = 0
            num_mcheck_noctr = 0
            num_nocheck =0
            for callsite in call.callsiteinfolist:
                if len(callsite.argcheckresult) == 0:
                    num_nocheck += 1
            r = 1-float(num_nocheck)/num_callsite
            if r >= r_1:
                s_out += "检查(%.2f) %s[%s] : ID = %s  "%(r,call.call_code,call.callsiteNums,call.call_id )
                print s_out
            #else:
                #s_out += "无检查(%.2f) %s[%s] : ID = %s  "%(r,call.call_code,call.callsiteNums,call.call_id )


    def getcheckstatistic(self,call):
        num_callsite =0
        num_scheck_ctr = 0
        num_scheck_noctr = 0
        num_mcheck_def = 0
        num_mcheck_ctr = 0
        num_mcheck_noctr = 0
        num_nocheck =0
        if(type(call) == list):
            for atomcall in call:
                s_out = ""
            s_out += "%s[%s] : ID = %s\n"%(atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
            i=0
            num_callsite = len(atomcall.callsiteinfolist)
            num_scheck_ctr = 0
            num_scheck_noctr = 0
            num_mcheck_def = 0
            num_mcheck_ctr = 0
            num_mcheck_noctr = 0
            num_nocheck =0
            for callsite in atomcall.callsiteinfolist:
                if(callsite.argcheckresult == "单参数检查-控制依赖"):
                    num_scheck_ctr += 1
                if(callsite.argcheckresult == "单参数检查-非控制条件"):
                    num_scheck_noctr += 1
                if(callsite.argcheckresult == "联合检查-相互定义"):
                    num_mcheck_def += 1
                if(callsite.argcheckresult == "联合检查-控制依赖"):
                    num_mcheck_ctr += 1
                if(callsite.argcheckresult == "联合检查-非控制条件"):
                    num_mcheck_noctr += 1
                if(callsite.argcheckresult == "无检查"):
                    num_nocheck += 1
            s_out += "\n单参数检查-控制依赖:%s"%num_scheck_ctr
            s_out += "\n单参数检查-非控制条件:%s"%num_scheck_noctr
            s_out += "\n联合检查-相互定义:%s"%num_mcheck_def
            s_out += "\n联合检查-控制依赖:%s"%num_mcheck_ctr
            s_out += "\n联合检查-非控制条件:%s"%num_mcheck_noctr
            s_out += "\n无检查:%s"%num_nocheck
            print s_out

        else:
            s_out = ""
            s_out += "%s[%s] : ID = %s\n"%(call.call_code,call.callsiteNums,call.call_id )
            i=0
            num_callsite = len(call.callsiteinfolist)
            num_scheck_ctr = 0
            num_scheck_noctr = 0
            num_mcheck_def = 0
            num_mcheck_ctr = 0
            num_mcheck_noctr = 0
            num_nocheck =0
            for callsite in call.callsiteinfolist:
                if(callsite.argcheckresult == "单参数检查-控制依赖"):
                    num_scheck_ctr += 1
                if(callsite.argcheckresult == "单参数检查-非控制条件"):
                    num_scheck_noctr += 1
                if(callsite.argcheckresult == "联合检查-相互定义"):
                    num_mcheck_def += 1
                if(callsite.argcheckresult == "联合检查-控制依赖"):
                    num_mcheck_ctr += 1
                if(callsite.argcheckresult == "联合检查-非控制条件"):
                    num_mcheck_noctr += 1
                if(callsite.argcheckresult == "无检查"):
                    num_nocheck += 1
            s_out += "\n单参数检查-控制依赖:%s"%num_scheck_ctr
            s_out += "\n单参数检查-控制依赖:%s"%num_scheck_noctr
            s_out += "\n单参数检查-控制依赖:%s"%num_mcheck_def
            s_out += "\n单参数检查-控制依赖:%s"%num_mcheck_ctr
            s_out += "\n单参数检查-控制依赖:%s"%num_mcheck_noctr
            s_out += "\n单参数检查-控制依赖:%s"%num_nocheck
            print s_out




    def LoadData(self,datapath):
        objfile = ObjDataAndBinFile()
        dbcalls = objfile.binfile2objdata(datapath)
        return dbcalls


    def printcheckinfo(self,call):
        if(type(call) == list):
            for atomcall in call:
                s_out = ""
                s_out += "%s[%s] : ID = %s\n"%(atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                i=0
                for callsite in atomcall.callsiteinfolist:
                    s_out += " %4d) "%i
                    s_out += "%s \'%s\' ID = %d\n"%(callsite.argcheckresult,callsite.call_code,callsite.call_id)
                    i = i+1
                print s_out
        else:
            s_out = ""
            s_out += "%s[%s] : ID = %s\n"%(call.call_code,call.callsiteNums,call.call_id )
            i=0
            for callsite in call.callsiteinfolist:
                s_out += " %4d) "%i
                s_out += "%s \'%s\' ID = %d\n"%(callsite.argcheckresult,callsite.call_code,callsite.call_id)
                i = i+1
            print s_out

    def printuncheckinfo(self,call):
        if(type(call) == list):
            for atomcall in call:
                s_out = ""
                s_out += "%s[%s] : ID = %s\n"%(atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                i=0
                for callsite in atomcall.callsiteinfolist:
                    if(len(callsite.argcheckresult) == 0):
                        s_out += " %4d) "%i
                        s_out += "%s \'%s\' ID = %d\n"%(callsite.argcheckresult,callsite.call_code,callsite.call_id)
                        i = i+1
                print s_out
        else:

                s_out = ""
                s_out += "%s[%s] : ID = %s\n"%(call.call_code,call.callsiteNums,call.call_id )
                i=0
                for callsite in call.callsiteinfolist:
                    if(len(callsite.argcheckresult) == 0):
                        s_out += " %4d) "%i
                        s_out += "%s \'%s\' ID = %d\n"%(callsite.argcheckresult,callsite.call_code,callsite.call_id)
                        i = i+1
                print s_out

    def printdatainfo(self,call):

        if(type(call) == list):
            for atomcall in call:
                s_out = ""
                s_out += "%s : NUM=%s : CALLID = %s\n"%(atomcall.call_code,atomcall.callsiteNums,atomcall.call_id )
                i=0
                for callsite in atomcall.callsiteinfolist:
                    s_out += "%6d) "%i
                    s_out += "%s \'%s\' ID = %d\n"%(callsite.argcheckresult,callsite.call_code,callsite.call_id)
                    s_out += "\t控制条件 = %s \n\t非控制条件 = %s \n"%(callsite.cndlistbycontrol, callsite.cndlistincfgpathNOcontrol)
                    s_out += "\t参数信息:\n"
                    for arg in callsite.argsinfolist:
                        s_out += "\t\t> \'%s\' ID = %s:\n"%(arg.code, arg.id)
                        s_out += "\t\t  symbol = %s:\n"%(arg.symbolset)
                        s_out += "\t\t  definestatments = %s:\n"%(arg.definestatments)
                        s_out += "\t\t  defvar = %s:\n"%(arg.defvar)
                    i = i+1
                print s_out
        else:
            s_out = ""
            s_out += "%s : NUM=%s : CALLID = %s\n"%(call.call_code,call.callsiteNums,call.call_id )
            i=0
            for callsite in call.callsiteinfolist:
                s_out += "%6d) "%i
                s_out += "%s \'%s\' ID = %d\n"%(callsite.argcheckresult,callsite.call_code,callsite.call_id)
                s_out += "\t控制条件 = %s \n\t非控制条件 = %s \n"%(callsite.cndlistbycontrol, callsite.cndlistincfgpathNOcontrol)
                s_out += "\t参数信息:\n"
                for arg in callsite.argsinfolist:
                    s_out += "\t\t> \'%s\' ID = %s:\n"%(arg.code, arg.id)
                    s_out += "\t\t  symbol = %s:\n"%(arg.symbolset)
                    s_out += "\t\t  definestatments = %s:\n"%(arg.definestatments)
                    s_out += "\t\t  defvar = %s:\n"%(arg.defvar)
                i = i+1
            print s_out

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    tool = displaydata()
    tool.run(sys.argv)

