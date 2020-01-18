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
from commonFile.ObjDataAndBinFile import ObjDataAndBinFile

import xlwt
import xlrd
import sampleFun

class analysisFeaturedata:
    def __init__(self):
        self.samples_sensitive = sampleFun.samples_sensitive
        self.samples_notsensitive = sampleFun.samples_notsensitive
        self.th_num = 4 #实例数量的阈值，只实例数量大于此值的函数进行识别
        return

    def write_excel(self,filename, data):
        book = xlwt.Workbook()            #创建excel对象
        sheet = book.add_sheet('PARTITIONS')  #添加一个表Sheet
        c = 0  #保存当前列
        for d in data: #取出data中的每一个元组存到表格的每一行
            sheet.write(c,0,d[0])
            for index in range(len(d[1])):   #将每一个元组中的每一个单元存到每一列
                sheet.write(c,index+1,d[1][index])
            c += 1
        book.save(filename) #保存excel

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
        elif len(cmd)==5 and cmd.__contains__("-x"):
            self.GetThesisData(cmd)
            return
        else:
            print "\n#功能: 依照DataStruct_intrap结构体对参数检查后的结构数据*_ConvertedData进行解析,提取相关信息."
            print "\n#用法:  xpoint_arg -datainfo  datapath callname  :获取callname的结构信息"
            print "\txpoint_arg -datainfo -a  datapath :获取所有函数的结构信息"
            print "\n\txpoint_arg -checkinfo datapath callname :获取callname的检查信息及其比例统计"
            print "\n\txpoint_arg -uncheckinfo datapath callname :获取callname的未检查信息及其比例统计"
            print "\txpoint_arg -checkinfo -a datapath :获取所有函数的检查信息及其比例统计"
            print "\n\txpoint_arg -checkedcall datapath ratio:获取比率为ratio设置下,参数检查的callname [有诸多变形]\n"
            print "\n\txpoint_arg -checkedcall2 datapath ratio_1 ratio_2:获取比率为[ratio_1,ratio_2]设置下,参数检查的callname [有诸多变形]\n"
            print "\n\txpoint_arg -checkstat datapath :获取各类参数检查的统计信息\n"
            print "\n\txpoint_arg -x datapath savedpath ratio :获取论文中需要的信息，存入savedpath\n"
        return

    def GetThesisData(self,cmd):
        savedpath = cmd[3]
        datapath = cmd[2]
        ratio = float(cmd[4])
        dbcalls = self.LoadData(datapath)
        f = open("../Data/%s"%savedpath,"w")
        fp_s= "../Data/s-%s.xls"%savedpath
        f_s= open("../Data/s-%s"%savedpath,"w")
        result_thesis = []
        print >> f, "函数总数量 = %d"%(dbcalls.numofcalls)
        num_calls_have_args = 0
        calllist_used_1 = [] #待识别的函数列表，有参数，实例数>1
        calllist_used_4 = [] #待识别的函数列表，有参数，实例数>4
        calllist_used_9 = [] #待识别的函数列表，有参数，实例数>9
        calllist_withcallee = [] #存在调用实例的函数列表
        calllist_withargs = [] #存在参数的函数列表
        calls_analysis = []
        num_calllist_used_1 = 0 #待识别的函数列表，有参数，实例数>1
        num_calllist_used_4 = 0 #待识别的函数列表，有参数，实例数>4
        num_calllist_used_9 = 0 #待识别的函数列表，有参数，实例数>9
        num_calllist_withcallee = 0 #存在调用实例的函数列表
        num_calllist_withargs = 0 #存在参数的函数列表

        print >> f, "函数名称 参数数量 实例数量 最多检查的参数序号 " \
                    "各参数[[显式的实例比例，隐式的实例比例，检查的实例比例] " \
                    "[显式的实例数量，隐式的实例数量，检查的实例数量]]" \
                    "AntMiner 算法1 算法2"
        print >> f_s, "函数名称 参数1 参数2 参数3 参数4 参数5"
        xpoints_arg_detail = []
        for call in dbcalls.callinfolist:
            callsiteNums = call.callsiteNums
            # 获取参数个数num_args，对于可变参数的函数，比如printf，将参数最多的实例的参数个数作为该函数的参数，
            # 在后续获取每个参数信息时候，不能以此处num_args作为实际参数数量，应该以具体实例数据作为实际数量。
            num_args = 0
            for callsite in call.callsiteinfolist:
                if num_args < len(callsite.argsinfolist):
                    num_args = len(callsite.argsinfolist)
                #print >> f, "\t%s"%(argcheck)

            if callsiteNums >0:
                calllist_withcallee.append([call,num_args])
            if num_args > 0 and callsiteNums > 0:
                calllist_withargs.append([call,num_args])
            if num_args > 0 and callsiteNums > 1:
                calllist_used_1.append([call,num_args])
            if num_args > 0 and callsiteNums > self.th_num:
                calls_analysis.append(call.call_code)
                calllist_used_4.append([call,num_args])
                result,result_s = self.GetCheckInfo_call(call, num_args, ratio)
                print >> f, result

                flag_checked = 0
                for r_args in result_s[1]:
                    if r_args == 1:
                        flag_checked = 1
                        break
                if flag_checked:
                    result_thesis.append(result_s)

                    #write_xls_add_line(f_s,result_s)
                    #tmp = ""
                    #for item in result_s[1]:
                    #    tmp = tmp + " %d"%item
                    #tmpstr = "%s\t%s"%(result_s[0],tmp)
                    #print >> f_s,tmpstr

                xpoints_arg_detail.append(result)

            if num_args > 0 and callsiteNums > 9:
                calllist_used_9.append([call,num_args])

        self.write_excel(fp_s,result_thesis)


        print >> f, "有实例的函数数量 = %d, 有参数及实例的函数数量 = %d, 实例数>1有参数函数数量 = %d, " \
                    "实例数>4有参数函数数量 = %d, 实例数>9有参数函数数量 = %d" %(
            len(calllist_withcallee),len(calllist_withargs),
            len(calllist_used_1), len(calllist_used_4),len(calllist_used_9))

        num_calls_antminer = 0;
        num_calls_alg1 = 0
        num_calls_alg2 = 0
        calls_antminer = []
        calls_alg1 = []
        for call_result in xpoints_arg_detail:
            if call_result[5] == 1:
                num_calls_antminer = num_calls_antminer + 1
                calls_antminer.append(call_result[0])
            if call_result[6] == 1:
                num_calls_alg1 = num_calls_alg1 + 1
                calls_alg1.append(call_result[0])
            if call_result[7] == 1:
                num_calls_alg2 = num_calls_alg2 + 1
        print >> f, "Antminer = %d, 算法1 = %d, 算法2 = %d, " %(
            num_calls_antminer,num_calls_alg1, num_calls_alg2)

            #print >> f, "\t%s\t%d\t%d"%(call_code, callsiteNums, num_args)
        f.close()
        """
        # 性能评估
        # 计算源代码项目中是实例数量大于th_num的基准函数个数
        num_samplesInprj_notsensitive = 0
        num_samplesInprj_sensitive = 0
        for call in calls_analysis:
            if call in self.samples_notsensitive:
                num_samplesInprj_notsensitive = num_samplesInprj_notsensitive + 1
            if call in self.samples_sensitive:
                num_samplesInprj_sensitive = num_samplesInprj_sensitive + 1
        print >> f_s, "num_samplesInprj_notsensitive = %d, " \
                      "num_samplesInprj_sensitive = %d"%(
                          num_samplesInprj_notsensitive,num_samplesInprj_sensitive)
        TP=0
        FP=0
        FN=0
        P=0
        R=0
        for icall in self.samples_sensitive:
            if icall in calls_analysis:
                flag_tp = 0
                for item in result_thesis:
                    if icall == item[0]:
                        TP = TP + 1
                        flag_tp = 1
                if flag_tp == 0:
                    FN = FN + 1

        for icall in self.samples_notsensitive:
            if icall in calls_analysis:
                for item in result_thesis:
                    if icall == item[0]:
                        FP = FP + 1

        P = round(float(TP)/(TP + FP),2)
        R = round(float(TP)/(TP + FN),2)
        """
        # 性能评估
        # 计算源代码项目中是实例数量大于th_num的基准函数个数
        num_samplesInprj_notsensitive = 0
        num_samplesInprj_sensitive = 0
        for call in calls_analysis:
            if call in self.samples_notsensitive:
                num_samplesInprj_notsensitive = num_samplesInprj_notsensitive + 1
            if call in self.samples_sensitive:
                num_samplesInprj_sensitive = num_samplesInprj_sensitive + 1
        print >> f_s, "num_samplesInprj_notsensitive = %d, " \
                      "num_samplesInprj_sensitive = %d"%(
                          num_samplesInprj_notsensitive,num_samplesInprj_sensitive)

        TP,FP,TN,FN,TPR,FPR = self.GetPandR(calls_analysis,calls_antminer)
        print >> f_s, "Antminer: TP=%d,FP=%d,TN=%d,FN=%d,TPR=%s,FPR=%s"%(
            TP,FP,TN,FN,TPR,FPR)
        TP,FP,TN,FN,TPR,FPR = self.GetPandR(calls_analysis,calls_alg1)
        print >> f_s, "Proposed: TP=%d,FP=%d,TN=%d,FN=%d,TPR=%s,FPR=%s"%(
            TP,FP,TN,FN,TPR,FPR)
        return

    def GetCheckInfo_call(self,callinfo, num_args, ratio):
        result = []
        result_s = []
        call_code = callinfo.call_code
        num_callsites = callinfo.callsiteNums
        argcheck_callsties = []
        for callsite in callinfo.callsiteinfolist:
            argcheckresult = callsite.argcheckresult
            # 解析实例中每个参数的显式检查和隐式检查,只区分以下情况
            # jointcheck-defstmt(i,j) 隐式检查
            # singlcheck-ctrlcnd(i) 显式检查
            # jointcheck-ctrlcnd(i,j) 显式检查
            # 每个参数的检查情况是列表[显式,隐式]，1表示有，0无，默认无
            arg_check = [[0,0] for i in range(num_args)]
            for argcheckinfo in argcheckresult:
                if "jointcheck-defstmt" in argcheckinfo:
                    i,j = self.getindex_JointImCheck(argcheckinfo)
                    arg_check[i][1] = 1
                    arg_check[j][1] = 1

                if "singlcheck-ctrlcnd" in argcheckinfo:
                    i = self.getindex_SingleExCheck(argcheckinfo)
                    arg_check[i][0] = 1

                if "jointcheck-ctrlcnd" in argcheckinfo:
                    i,j = self.getindex_JointExCheck(argcheckinfo)
                    arg_check[i][0] = 1
                    arg_check[j][0] = 1
            argcheck_callsties.append(arg_check)

        num_callsites_explicit = 0
        num_callsites_implicit = 0
        num_callsites_check = 0
        args_checkresult = [[] for i in range(num_args)]
        args_checkresult_simple = [[] for i in range(num_args)]


        for arg_index in range(0,num_args):
            num_callsites_explicit = 0
            num_callsites_implicit = 0
            num_callsites_check = 0
            for check in argcheck_callsties:
                if check[arg_index][0] == 1:
                    num_callsites_explicit = num_callsites_explicit+1
                if check[arg_index][1] == 1:
                    num_callsites_implicit = num_callsites_implicit+1
                if check[arg_index][0] == 1 or check[arg_index][1] == 1:
                    num_callsites_check = num_callsites_check + 1
            # path_ratio = round(float(feature[2][0])/feature[3][0],3)
            ratio_ex = round(float(num_callsites_explicit)/num_callsites,2)
            ratio_im = round(float(num_callsites_implicit)/num_callsites,2)
            ratio_check = round(float(num_callsites_check)/num_callsites,2)
            args_checkresult_item = [ratio_ex,ratio_im,ratio_check]
            args_checkresult_nums = [num_callsites_explicit,
                                     num_callsites_implicit,num_callsites_check]
            args_checkresult[arg_index] = [args_checkresult_item,args_checkresult_nums]
            if ratio_check >= ratio:
                args_checkresult_simple[arg_index] = 1
            else:
                args_checkresult_simple[arg_index] = 0

        tmp_ratio_callsites = 0
        argIndex_most_check = 0
        # 找出被检查最多的参数序号
        for arg_index in range(0,num_args):
            if args_checkresult[arg_index][0][2] > tmp_ratio_callsites:
                tmp_ratio_callsites = args_checkresult[arg_index][0][2]
                argIndex_most_check = arg_index

        ischecked_ex = 0 # 只考虑显示检查的antminer
        ischecked_alg1 = 0 # 不考虑优先级的算法1
        ischecked_alg2 = 0 #考虑优先级的算法2

        if args_checkresult[argIndex_most_check][0][0] >= ratio:
            ischecked_ex = 1
        if args_checkresult[argIndex_most_check][0][2] >= ratio:
            ischecked_alg1 = 1

        # 查看参数是否为指针类型
        if ischecked_alg1 == 1:
            for callsite in callinfo.callsiteinfolist:
                for arginfo in callsite.argsinfolist:
                    if  '[' in arginfo.defvar:
                        ischecked_alg2 = 1
                    if  '*' in arginfo.defvar:
                        ischecked_alg2 = 1
                    if  '->' in arginfo.defvar:
                        ischecked_alg2 = 1
                    break
                if ischecked_alg2 == 1:
                    break

        result.append(call_code)
        result.append(num_args)
        result.append(num_callsites)
        result.append(argIndex_most_check)#最多检查的参数序号
        #最多检查参数的被检查情况：显式，隐式，显式或隐式
        #result.append(args_checkresult[argIndex_most_check])
        result.append(args_checkresult)
        result.append(ischecked_ex) # 只考虑显示检查的antminer
        result.append(ischecked_alg1) # 不考虑优先级的算法1
        result.append(ischecked_alg2) #考虑优先级的算法2

        result_s.append(call_code)
        result_s.append(args_checkresult_simple)
        return result,result_s

    def GetPandR(self,calls_all,calls_sensitive):

        TP=0
        FP=0
        TN=0
        FN=0
        TPR=0
        FPR=0
        for icall in self.samples_sensitive:
            if icall in calls_all:
                if icall in calls_sensitive:
                    TP = TP + 1
                else:
                    FN = FN + 1

        for icall in self.samples_notsensitive:
            if icall in calls_all:
                if icall in calls_sensitive:
                    FP = FP + 1
                else:
                    TN = TN + 1

        TPR = round(float(TP)/(TP + FN),2)
        FPR = round(float(FP)/(FP + TN),2)
        #print >> f_s, "TP=%d,FP=%d,TN=%d,FN=%d,TPR=%s,FPR=%s"%(TP,FP,FN,P,R)

        return TP,FP,TN,FN,TPR,FPR


    def getindex_JointImCheck(self,argcheck):
        #i = argcheck[len("jointcheck-defstmt(")]
        #j = argcheck[len("jointcheck-defstmt(i,")]
        start = argcheck.index('(')
        last = argcheck.index(',')
        i = argcheck[start+1:last]
        start = argcheck.index(',')
        last = argcheck.index(')')
        j = argcheck[start+1:last]
        return int(i),int(j)

    def getindex_SingleExCheck(self,argcheck):
        start = argcheck.index('(')
        last = argcheck.index(')')
        i = argcheck[start+1:last]
        return int(i)

    def getindex_JointExCheck(self,argcheck):
        start = argcheck.index('(')
        last = argcheck.index(',')
        i = argcheck[start+1:last]
        start = argcheck.index(',')
        last = argcheck.index(')')
        j = argcheck[start+1:last]
        return int(i),int(j)


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
    tool = analysisFeaturedata()
    tool.run(sys.argv)

