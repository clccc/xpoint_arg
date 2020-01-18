#code by CkMeanshenlin 2016-03-26
#coding:utf-8
# 外部检测的软件度量,3
import os
import time
from numpy import *
import commonFile.DataStruct as DataStruct
import commonFile.DataStruct_D as DataStruct_D
import commonFile.OPS_DataStruct as OPS_DataStruct
from commonFile.ObjDataAndBinFile import ObjDataAndBinFile


class   xPoint:
    def run(self,filename,k):
        """"
        每类对象的x矢量：
            对象实例的预处理力度 pDealIntensity_calleeg.
            对象的预处理力度均值
            对象的实例个数／代码量总函数实例个数
            参数敏感度
            对象对参数的内处理力度
        """

        #self.knn(filename,k,self.GenVector_1)
        #self.knn(filename,k,self.GenVector_2)
        #self.knn(filename,k,self.GenVector_3)
        #self.knn(filename,k,self.GenVector_4)
        #self.knn(filename,k,self.GenVector_5)
        ##self.knn(filename,k,self.GenVectorD_5)
        ##self.knn(filename,k,self.GenVectorD_6)
        #self.knn(filename,k,self.GenVectorD_7) #3维 1191:5035,目前最好结果了,1191为目标分类
        self.knn(filename,k,self.GenVectorD_8)
        #self.knn(filename,k,self.GenVectorD_9) #4维 1123:5103
        #self.knn(filename,k,self.GenVectorD_10) #3维 1081:5145 knn_20160630201617

        print '结束'

    def knn(self,filename,k,GenVector):
        #callinfo = self.GenVector_1(filename)
        dataSource = GenVector(filename)
        tmp_list = []
        for call in dataSource:
            tmp_list.append(call[3:len(call)])#前2列为call的id和code,参考信息.排除
        dataArray=array(tmp_list)

        import kMeans
        centroids, clusterAssment = kMeans.kMeans(dataArray, k)
        clusterlist = clusterAssment.tolist()
        list_knn=[]

        for i in range(0,len(dataSource)):
            #f.write(callinfo[i][0])
            list_knn.append(clusterlist[i]+dataSource[i])

        resultdir = "../Data/knn_%s/"%time.strftime('%Y%m%d%H%M%S')
        os.mkdir(resultdir)
        f = open(resultdir+"knn_result.txt",'w')
        for list_item in list_knn:
            f.write(str(list_item))
            f.write("\n")
        f.close()

        num = [0]*k
        for i in range(0,k):
            f_name = resultdir+"knn_result_%s.txt"%i
            f_k = open(f_name,'w')
            for list_item in list_knn:
                if(list_item[0] == i):
                    num[i] = num[i]+1
                    f_k.write(str(list_item))
                    f_k.write("\n")
            f_k.close()

        s_out = ""
        s_out += "k-均值聚类结束!\n"
        s_out += "数据源文件:\n\t%s\n"%filename
        s_out += "特征向量提取方法:\n\t%s\n"%GenVector
        s_out += "样本量:\n\t%d\n"%len(list_knn)
        s_out += "类别数量:\n\tk = %d \n"%k
        s_out += "结果文件为(位置:%s):\n\tlog.txt (执行日志)\n\tknn_result.txt (总的聚类结果)\n"%resultdir
        for i in range(0,k):
            s_out +="\tknn_result_%d.txt "%i
            s_out +=" (l = %d)\n"%num[i]

        print s_out
        f = open(resultdir+"log.txt",'w')
        f.write(s_out)
        f.close()

        return
    #--------------------------
    #GenVector_1
    #特征向量提取:3维 callee被调用前的条件语句数量,callee实参参与的运算语句数量,callee实参参与的条件语句数量.
    #备注:涉及参数的均为各参数值的累加;所有分量均会除以callee的调用次数,即均值
    #向量是否归一化:否
    #--------------------------
    def GenVector_1(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = OPS_DataStruct.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        args_leaves_num = []
        args_cnd_num = []
        tmp_args_leaves_num = 0
        tmp_args_cnd_num = 0
        tmp_call_cnd_num =0
        for call in dbcalls.callinfolist:
            tmp_args_leaves_num = 0
            tmp_args_cnd_num = 0
            tmp_call_cnd_num =0
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:

                    tmp_args_leaves_num = tmp_args_leaves_num + len(arginfo.arg_leavesIdlist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condIds)
            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),4),
                                 round(tmp_args_leaves_num/float(call.callsiteNums),4),
                                 round(tmp_args_cnd_num/float(call.callsiteNums),4)
                                 ])
        return callinfo

    #--------------------------
    #GenVector_2:
    #特征向量提取:3维 callee被调用前的条件语句数量,callee实参参与的运算语句数量,callee实参参与的条件语句数量.
    #备注:涉及参数的均为各参数值的累加;所有分量均会除以callee的调用次数,即均值
    #向量是否归一化:是
    #--------------------------
    def GenVector_2(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = OPS_DataStruct.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        args_leaves_num = []
        args_cnd_num = []
        tmp_args_leaves_num = 0
        tmp_args_cnd_num = 0
        tmp_call_cnd_num =0
        for call in dbcalls.callinfolist:
            tmp_args_leaves_num = 0
            tmp_args_cnd_num = 0
            tmp_call_cnd_num =0
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:

                    tmp_args_leaves_num = tmp_args_leaves_num + len(arginfo.arg_leavesIdlist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condIds)
            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),4),
                                 round(tmp_args_leaves_num/float(call.callsiteNums),4),
                                 round(tmp_args_cnd_num/float(call.callsiteNums),4)
                                 ])

        datamax = [callinfo[0][3],callinfo[0][4],callinfo[0][5]]
        datamin = [callinfo[0][3],callinfo[0][4],callinfo[0][5]]

        for callitem in callinfo:
            for i in range(3,len(callitem)):
                if callitem[i] > datamax[i-3]:
                    datamax[i-3] = callitem[i]
                if callitem[i] < datamin[i-3]:
                    datamin[i-3] = callitem[i]

        for callitem in callinfo:
            for i in range(3,len(callitem)):
                if ((datamax[i-3]-datamin[i-3]) !=0):
                 callitem[i] = round((callitem[i]- datamin[i-3])/(datamax[i-3]-datamin[i-3]),4)
        print "datamax=:",datamax
        print "datamin=:",datamin
        return callinfo

    #--------------------------
    #GenVector_3:
    #特征向量提取:5维
    #       callee被调用前的条件语句数量
    #       callee实参参与的运算语句数量
    #       callee实参参与的条件语句数量
    #       callee实参共同参与的运算语句数量
    #       callee实参共同参与的条件语句数量
    #备注:涉及参数的均为各参数值的累加;所有分量均会除以callee的调用次数,即均值
    #向量是否归一化:是
    #--------------------------
    def GenVector_3(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = OPS_DataStruct.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        args_leaves_num = []
        args_cnd_num = []

        tmp_args_leaves_num = 0
        tmp_args_cnd_num = 0
        tmp_args_coleaves_num = 0
        tmp_args_cocnds_num = 0

        tmp_call_cnd_num =0
        for call in dbcalls.callinfolist:
            tmp_args_leaves_num = 0
            tmp_args_cnd_num = 0
            tmp_call_cnd_num =0
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:
                    tmp_args_leaves_num = tmp_args_leaves_num + len(arginfo.arg_leavesIdlist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condIds)

                tmp_args_coleaves_list = []
                tmp_args_cocnds_list = []
                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        if(i != j):
                            for val_leaf in callsite.callsite_argsinfolist[i].arg_leavesIdlist:
                                 if val_leaf in callsite.callsite_argsinfolist[j].arg_leavesIdlist:
                                    tmp_args_coleaves_list.append(val_leaf)

                            for val_cnd in callsite.callsite_argsinfolist[i].arg_condIds:
                                if val_cnd in callsite.callsite_argsinfolist[j].arg_condIds:
                                    tmp_args_cocnds_list.append(val_cnd)
                tmp_args_coleaves_num = len(tmp_args_coleaves_list)#未去重
                tmp_args_cocnds_num = len(tmp_args_cocnds_list)#未去重

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),4),
                                 round(tmp_args_leaves_num/float(call.callsiteNums),4),
                                 round(tmp_args_cnd_num/float(call.callsiteNums),4),
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),4),
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),4)
                                 ])

        datamax = [callinfo[0][3],callinfo[0][4],callinfo[0][5],callinfo[0][6],callinfo[0][7]]
        datamin = [callinfo[0][3],callinfo[0][4],callinfo[0][5],callinfo[0][6],callinfo[0][7]]

        for callitem in callinfo:
            for i in range(3,len(callitem)):
                if callitem[i] > datamax[i-3]:
                    datamax[i-3] = callitem[i]
                if callitem[i] < datamin[i-3]:
                    datamin[i-3] = callitem[i]

        for callitem in callinfo:
            for i in range(3,len(callitem)):
                if ((datamax[i-3]-datamin[i-3]) !=0):
                 callitem[i] = round((callitem[i]- datamin[i-3])/(datamax[i-3]-datamin[i-3]),4)
        return callinfo

    #--------------------------
    #GenVector_4:
    #特征向量提取:5维
    #       callee被调用前的条件语句数量
    #       callee实参参与的运算语句数量
    #       callee实参参与的条件语句数量
    #       callee实参共同参与的运算语句数量
    #       callee实参共同参与的条件语句数量
    #备注:涉及参数的均为各参数值的累加;所有分量均会除以callee的调用次数,即均值
    #向量是否归一化:否
    #--------------------------
    def GenVector_4(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = OPS_DataStruct.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        args_leaves_num = []
        args_cnd_num = []

        tmp_args_leaves_num = 0
        tmp_args_cnd_num = 0
        tmp_args_coleaves_num = 0
        tmp_args_cocnds_num = 0

        tmp_call_cnd_num =0
        for call in dbcalls.callinfolist:
            tmp_args_leaves_num = 0
            tmp_args_cnd_num = 0
            tmp_call_cnd_num =0
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:
                    tmp_args_leaves_num = tmp_args_leaves_num + len(arginfo.arg_leavesIdlist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condIds)

                tmp_args_coleaves_list = []
                tmp_args_cocnds_list = []
                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        if(i != j):
                            for val_leaf in callsite.callsite_argsinfolist[i].arg_leavesIdlist:
                                 if val_leaf in callsite.callsite_argsinfolist[j].arg_leavesIdlist:
                                    tmp_args_coleaves_list.append(val_leaf)

                            for val_cnd in callsite.callsite_argsinfolist[i].arg_condIds:
                                if val_cnd in callsite.callsite_argsinfolist[j].arg_condIds:
                                    tmp_args_cocnds_list.append(val_cnd)
                tmp_args_coleaves_num = len(tmp_args_coleaves_list)#未去重
                tmp_args_cocnds_num = len(tmp_args_cocnds_list)#未去重

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),4),
                                 round(tmp_args_leaves_num/float(call.callsiteNums),4),
                                 round(tmp_args_cnd_num/float(call.callsiteNums),4),
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),4),
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),4)
                                 ])
        '''
        datamax = [callinfo[0][3],callinfo[0][4],callinfo[0][5],callinfo[0][6],callinfo[0][7]]
        datamin = [callinfo[0][3],callinfo[0][4],callinfo[0][5],callinfo[0][6],callinfo[0][7]]

        for callitem in callinfo:
            for i in range(3,len(callitem)):
                if callitem[i] > datamax[i-3]:
                    datamax[i-3] = callitem[i]
                if callitem[i] < datamin[i-3]:
                    datamin[i-3] = callitem[i]

        for callitem in callinfo:
            for i in range(3,len(callitem)):
                if ((datamax[i-3]-datamin[i-3]) !=0):
                 callitem[i] = round((callitem[i]- datamin[i-3])/(datamax[i-3]-datamin[i-3]),4)
        '''
        return callinfo

    #--------------------------
    #GenVector_5:
    #特征向量提取:5维
    #       callee被调用前的条件语句是否存在
    #       callee实参参与的左侧运算语句是否存在
    #       callee实参参与的右侧运算语句是否存在
    #       callee实参参与的call语句是否存在
    #       callee实参参与的条件语句是否存在
    #       callee实参共同参与的运算语句是否存在
    #       callee实参共同参与的条件语句是否存在
    #向量是否归一化:否
    #--------------------------
    def GenVector_5(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = OPS_DataStruct.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        args_leaves_num = []
        args_cnd_num = []

        tmp_args_leaves_num = 0
        tmp_args_cnd_num = 0
        tmp_args_coleaves_num = 0
        tmp_args_cocnds_num = 0

        tmp_call_cnd_num =0
        for call in dbcalls.callinfolist:
            tmp_args_leaves_num = 0
            tmp_args_cnd_num = 0
            tmp_call_cnd_num =0
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:
                    tmp_args_leaves_num = tmp_args_leaves_num + len(arginfo.arg_leavesIdlist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condIds)

                tmp_args_coleaves_list = []
                tmp_args_cocnds_list = []
                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        if(i != j):
                            for val_leaf in callsite.callsite_argsinfolist[i].arg_leavesIdlist:
                                 if val_leaf in callsite.callsite_argsinfolist[j].arg_leavesIdlist:
                                    tmp_args_coleaves_list.append(val_leaf)

                            for val_cnd in callsite.callsite_argsinfolist[i].arg_condIds:
                                if val_cnd in callsite.callsite_argsinfolist[j].arg_condIds:
                                    tmp_args_cocnds_list.append(val_cnd)
                tmp_args_coleaves_num = len(tmp_args_coleaves_list)#未去重
                tmp_args_cocnds_num = len(tmp_args_cocnds_list)#未去重

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_call_cnd_num > 0 else 0,
                                 1 if tmp_args_leaves_num > 0 else 0,
                                 1 if tmp_args_cnd_num > 0 else 0,
                                 1 if tmp_args_coleaves_num > 0 else 0,
                                 1 if tmp_args_cocnds_num > 0 else 0
                                 ])

        return callinfo


    #--------------------------
    #GenVectorD_5:针对包含更精细的实参分析的原始数据文件
    #特征向量提取:5维
    #       callee被调用前的条件语句是否存在
    #       callee实参参与的左侧运算语句是否存在
    #       callee实参参与的右侧运算语句是否存在
    #       callee实参参与的call语句是否存在
    #       callee实参参与的条件语句是否存在
    #       callee实参共同参与的运算语句是否存在(左侧,右侧必须各有一个实参相关的symbol,直接相关)
    #       callee实参共同参与的条件语句是否存在
    #向量是否归一化:否
    #--------------------------
    def GenVectorD_5(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = DataStruct_D.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        for call in dbcalls.callinfolist:
            tmp_call_cnd_num = 0
            tmp_args_stmtsleft_num = 0
            tmp_args_stmtsright_num = 0
            tmp_args_stmtscall_num = 0
            tmp_args_cnd_num = 0
            tmp_args_coleaves_num = 0
            tmp_args_cocnds_num = 0
            tmp_args_cocnds_list = []
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:
                    tmp_args_stmtsleft_num += len(arginfo.arg_stmtsleftlist)
                    tmp_args_stmtsright_num += len(arginfo.arg_stmtsrightlist)
                    tmp_args_stmtscall_num += len(arginfo.arg_stmtiscalllist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condidlist)
                flag_coleaves = False
                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        for val_leaf in callsite.callsite_argsinfolist[i].arg_stmtsleftlist:
                             if val_leaf in callsite.callsite_argsinfolist[j].arg_stmtsrightlist:
                                flag_coleaves = True
                        #如果处于共同的call中,也视为相互定义
                        for val_call in callsite.callsite_argsinfolist[i].arg_stmtiscalllist:
                             if val_call in callsite.callsite_argsinfolist[j].arg_stmtiscalllist:
                                flag_coleaves = True
                        if(flag_coleaves):
                            tmp_args_coleaves_num +=1
                            flag_coleaves = False

                        for val_cnd in callsite.callsite_argsinfolist[i].arg_condidlist:
                            if val_cnd in callsite.callsite_argsinfolist[j].arg_condidlist:
                                tmp_args_cocnds_list.append(val_cnd)


                tmp_args_cocnds_num = len(tmp_args_cocnds_list)#未去重

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 tmp_call_cnd_num,
                                 tmp_args_stmtsleft_num ,
                                 tmp_args_stmtsright_num ,
                                 tmp_args_stmtscall_num ,
                                 tmp_args_cnd_num ,
                                 tmp_args_coleaves_num ,
                                 tmp_args_cocnds_num
                                 ])
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_call_cnd_num > 0 else 0,
                                 1 if tmp_args_stmtsleft_num > 0 else 0,
                                 1 if tmp_args_stmtsright_num > 0 else 0,
                                 1 if tmp_args_stmtscall_num > 0 else 0,
                                 1 if tmp_args_cnd_num > 0 else 0,
                                 1 if tmp_args_coleaves_num > 0 else 0,
                                 1 if tmp_args_cocnds_num > 0 else 0
                                 ])

        return callinfo

    #--------------------------
    #GenVectorD_6:针对包含更精细的实参分析的原始数据文件
    #特征向量提取:5维
    #       callee被调用前的条件语句是否存在
    #       callee实参参与的左侧运算语句是否存在
    #       callee实参参与的条件语句是否存在
    #       callee实参共同参与的运算语句是否存在(左侧,右侧必须各有一个实参相关的symbol,直接相关)
    #       callee实参共同参与的条件语句是否存在
    #向量是否归一化:否
    #--------------------------
    def GenVectorD_6(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = DataStruct_D.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        for call in dbcalls.callinfolist:
            tmp_call_cnd_num = 0
            tmp_args_stmtsleft_num = 0
            tmp_args_stmtsright_num = 0
            tmp_args_stmtscall_num = 0
            tmp_args_cnd_num = 0
            tmp_args_coleaves_num = 0
            tmp_args_cocnds_num = 0
            tmp_args_cocnds_list = []
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:
                    tmp_args_stmtsleft_num += len(arginfo.arg_stmtsleftlist)
                    tmp_args_stmtsright_num += len(arginfo.arg_stmtsrightlist)
                    tmp_args_stmtscall_num += len(arginfo.arg_stmtiscalllist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condidlist)
                flag_coleaves = False
                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        for val_leaf in callsite.callsite_argsinfolist[i].arg_stmtsleftlist:
                             if val_leaf in callsite.callsite_argsinfolist[j].arg_stmtsrightlist:
                                flag_coleaves = True
                        #如果处于共同的call中,也视为相互定义
                        for val_call in callsite.callsite_argsinfolist[i].arg_stmtiscalllist:
                             if val_call in callsite.callsite_argsinfolist[j].arg_stmtiscalllist:
                                flag_coleaves = True
                        if(flag_coleaves):
                            tmp_args_coleaves_num +=1
                            flag_coleaves = False

                        for val_cnd in callsite.callsite_argsinfolist[i].arg_condidlist:
                            if val_cnd in callsite.callsite_argsinfolist[j].arg_condidlist:
                                tmp_args_cocnds_list.append(val_cnd)


                tmp_args_cocnds_num = len(tmp_args_cocnds_list)#未去重

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 tmp_call_cnd_num,
                                 tmp_args_stmtsleft_num ,
                                 tmp_args_stmtsright_num ,
                                 tmp_args_stmtscall_num ,
                                 tmp_args_cnd_num ,
                                 tmp_args_coleaves_num ,
                                 tmp_args_cocnds_num
                                 ])
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_call_cnd_num > 0 else 0,
                                 1 if tmp_args_stmtsleft_num > 0 else 0,
                                 1 if tmp_args_cnd_num > 0 else 0,
                                 1 if tmp_args_coleaves_num > 0 else 0,
                                 1 if tmp_args_cocnds_num > 0 else 0
                                 ])

        return callinfo

    #--------------------------
    #GenVectorD_7:针对包含更精细的实参分析的原始数据文件
    #特征向量提取:5维
    #       callee实参参与的条件语句是否存在
    #       callee实参共同参与的运算语句是否存在(左侧,右侧必须各有一个实参相关的symbol,直接相关)
    #       callee实参共同参与的条件语句是否存在
    #向量是否归一化:否
    #--------------------------
    def GenVectorD_7(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = DataStruct_D.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        for call in dbcalls.callinfolist:
            tmp_call_cnd_num = 0
            tmp_args_stmtsleft_num = 0
            tmp_args_stmtsright_num = 0
            tmp_args_stmtscall_num = 0
            tmp_args_cnd_num = 0
            tmp_args_coleaves_num = 0
            tmp_args_cocnds_num = 0
            tmp_args_cocnds_list = []
            for callsite in call.callsiteinfolist:
                tmp_call_cnd_num = tmp_call_cnd_num + len(callsite.callsite_conditionslist)
                for arginfo in callsite.callsite_argsinfolist:
                    tmp_args_stmtsleft_num += len(arginfo.arg_stmtsleftlist)
                    tmp_args_stmtsright_num += len(arginfo.arg_stmtsrightlist)
                    tmp_args_stmtscall_num += len(arginfo.arg_stmtiscalllist)
                    tmp_args_cnd_num = tmp_args_cnd_num + len(arginfo.arg_condidlist)
                flag_coleaves = False
                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        for val_leaf in callsite.callsite_argsinfolist[i].arg_stmtsleftlist:
                             if val_leaf in callsite.callsite_argsinfolist[j].arg_stmtsrightlist:
                                flag_coleaves = True
                        #如果处于共同的call中,也视为相互定义
                        for val_call in callsite.callsite_argsinfolist[i].arg_stmtiscalllist:
                             if val_call in callsite.callsite_argsinfolist[j].arg_stmtiscalllist:
                                flag_coleaves = True
                        if(flag_coleaves):
                            tmp_args_coleaves_num +=1
                            flag_coleaves = False

                        for val_cnd in callsite.callsite_argsinfolist[i].arg_condidlist:
                            if val_cnd in callsite.callsite_argsinfolist[j].arg_condidlist:
                                tmp_args_cocnds_list.append(val_cnd)


                tmp_args_cocnds_num = len(tmp_args_cocnds_list)#未去重

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 tmp_call_cnd_num,
                                 tmp_args_stmtsleft_num ,
                                 tmp_args_stmtsright_num ,
                                 tmp_args_stmtscall_num ,
                                 tmp_args_cnd_num ,
                                 tmp_args_coleaves_num ,
                                 tmp_args_cocnds_num
                                 ])
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_args_cnd_num > 0 else 0,
                                 1 if tmp_args_coleaves_num > 0 else 0,
                                 1 if tmp_args_cocnds_num > 0 else 0
                                 ])

        return callinfo

    #--------------------------
    #GenVectorD_8:针对包含更精细的实参分析的原始数据文件
    #特征向量提取:5维
    #       callee实参参与的条件语句是否过半存在
    #       callee实参共同参与的运算语句是否过半存在(左侧,右侧必须各有一个实参相关的symbol,直接相关)
    #       callee实参共同参与的条件语句是否过半存在
    #向量是否归一化:否
    #--------------------------
    def GenVectorD_8(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = DataStruct_D.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        for call in dbcalls.callinfolist:
            tmp_call_cnd_num = 0
            tmp_args_stmtsleft_num = 0
            tmp_args_stmtsright_num = 0
            tmp_args_stmtscall_num = 0
            tmp_args_cnd_num = 0
            tmp_args_coleaves_num = 0
            tmp_args_cocnds_num = 0
            tmp_args_cocnds_list = []



            for callsite in call.callsiteinfolist:
                flag_args_stmtsleft = False
                flag_args_stmtsright = False
                flag_args_stmtscall = False
                flag_args_cnd = False
                flag_coleaves = False
                flag_args_cocnds = False
                if(len(callsite.callsite_conditionslist) > 0):
                    tmp_call_cnd_num += 1
                for arginfo in callsite.callsite_argsinfolist:
                    if (len(arginfo.arg_stmtsleftlist) >= 1):
                        flag_args_stmtsleft = True
                    if (len(arginfo.arg_stmtsrightlist) >= 1):
                        flag_args_stmtsright = True
                    if (len(arginfo.arg_stmtiscalllist) >= 1):
                        flag_args_stmtscall = True
                    if (len(arginfo.arg_condidlist) >= 1):
                        flag_args_cnd= True

                if(flag_args_stmtsleft):
                    tmp_args_stmtsleft_num +=1
                if(flag_args_stmtsright):
                    tmp_args_stmtsright_num +=1
                if(flag_args_stmtscall):
                    tmp_args_stmtscall_num +=1
                if(flag_args_cnd):
                    tmp_args_cnd_num +=1


                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        for val_leaf in callsite.callsite_argsinfolist[i].arg_stmtsleftlist:
                             if val_leaf in callsite.callsite_argsinfolist[j].arg_stmtsrightlist:
                                flag_coleaves = True
                        #如果处于共同的call中,也视为相互定义
                        for val_call in callsite.callsite_argsinfolist[i].arg_stmtiscalllist:
                             if val_call in callsite.callsite_argsinfolist[j].arg_stmtiscalllist:
                                flag_coleaves = True


                        for val_cnd in callsite.callsite_argsinfolist[i].arg_condidlist:
                            if val_cnd in callsite.callsite_argsinfolist[j].arg_condidlist:
                                flag_args_cocnds = True

                if(flag_coleaves):
                    tmp_args_coleaves_num +=1
                    flag_coleaves = False
                if(flag_args_cocnds):
                    tmp_args_cocnds_num +=1
                    flag_args_cocnds = False

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 tmp_call_cnd_num,
                                 tmp_args_stmtsleft_num ,
                                 tmp_args_stmtsright_num ,
                                 tmp_args_stmtscall_num ,
                                 tmp_args_cnd_num ,
                                 tmp_args_coleaves_num ,
                                 tmp_args_cocnds_num
                                 ])
            '''

            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_args_cnd_num > call.callsiteNums*0.7 else 0,
                                 1 if tmp_args_coleaves_num > call.callsiteNums*0.7 else 0,
                                 1 if tmp_args_cocnds_num > call.callsiteNums*0.7 else 0
                                 ])
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_args_cnd_num > call.callsiteNums*0.7 else 0,
                                 1 if tmp_args_coleaves_num > call.callsiteNums*0.7 else 0,
                                 1 if tmp_args_cocnds_num > call.callsiteNums*0.7 else 0
                                 ])
            '''

            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),3),
                                 round(tmp_args_stmtsleft_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_stmtsright_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_stmtscall_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cnd_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),3)
                                 ])
            '''
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),3),
                                 round(tmp_args_cnd_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),3)
                                 ])
            '''


        return callinfo


    #--------------------------
    #GenVectorD_9:针对包含更精细的实参分析的原始数据文件
    #特征向量提取:4维
    #       callee调用前存在条件语句的频率
    #       callee实参参与的条件语句在Callsite存在的频率(即计算出现过Callsite的比率)
    #       callee实参共同参与的运算语句在Callsite存在的频率(左侧,右侧必须各有一个实参相关的symbol,直接相关)
    #       callee实参共同参与的条件语句在Callsite存在的频率
    #向量是否归一化:否
    #--------------------------
    def GenVectorD_9(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = DataStruct_D.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        for call in dbcalls.callinfolist:
            tmp_call_cnd_num = 0
            tmp_args_stmtsleft_num = 0
            tmp_args_stmtsright_num = 0
            tmp_args_stmtscall_num = 0
            tmp_args_cnd_num = 0
            tmp_args_coleaves_num = 0
            tmp_args_cocnds_num = 0
            tmp_args_cocnds_list = []



            for callsite in call.callsiteinfolist:
                flag_args_stmtsleft = False
                flag_args_stmtsright = False
                flag_args_stmtscall = False
                flag_args_cnd = False
                flag_coleaves = False
                flag_args_cocnds = False
                if(len(callsite.callsite_conditionslist) > 0):
                    tmp_call_cnd_num += 1
                for arginfo in callsite.callsite_argsinfolist:
                    if (len(arginfo.arg_stmtsleftlist) >= 1):
                        flag_args_stmtsleft = True
                    if (len(arginfo.arg_stmtsrightlist) >= 1):
                        flag_args_stmtsright = True
                    if (len(arginfo.arg_stmtiscalllist) >= 1):
                        flag_args_stmtscall = True
                    if (len(arginfo.arg_condidlist) >= 1):
                        flag_args_cnd= True

                if(flag_args_stmtsleft):
                    tmp_args_stmtsleft_num +=1
                if(flag_args_stmtsright):
                    tmp_args_stmtsright_num +=1
                if(flag_args_stmtscall):
                    tmp_args_stmtscall_num +=1
                if(flag_args_cnd):
                    tmp_args_cnd_num +=1


                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        for val_leaf in callsite.callsite_argsinfolist[i].arg_stmtsleftlist:
                             if val_leaf in callsite.callsite_argsinfolist[j].arg_stmtsrightlist:
                                flag_coleaves = True
                        #如果处于共同的call中,也视为相互定义
                        for val_call in callsite.callsite_argsinfolist[i].arg_stmtiscalllist:
                             if val_call in callsite.callsite_argsinfolist[j].arg_stmtiscalllist:
                                flag_coleaves = True


                        for val_cnd in callsite.callsite_argsinfolist[i].arg_condidlist:
                            if val_cnd in callsite.callsite_argsinfolist[j].arg_condidlist:
                                flag_args_cocnds = True

                if(flag_coleaves):
                    tmp_args_coleaves_num +=1
                    flag_coleaves = False
                if(flag_args_cocnds):
                    tmp_args_cocnds_num +=1
                    flag_args_cocnds = False

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 tmp_call_cnd_num,
                                 tmp_args_stmtsleft_num ,
                                 tmp_args_stmtsright_num ,
                                 tmp_args_stmtscall_num ,
                                 tmp_args_cnd_num ,
                                 tmp_args_coleaves_num ,
                                 tmp_args_cocnds_num
                                 ])
            '''
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_args_cnd_num > call.callsiteNums/2 else 0,
                                 1 if tmp_args_coleaves_num > call.callsiteNums/2 else 0,
                                 1 if tmp_args_cocnds_num > call.callsiteNums/2 else 0
                                 ])
            '''
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),3),
                                 round(tmp_args_stmtsleft_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_stmtsright_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_stmtscall_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cnd_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),3)
                                 ])
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),3),
                                 round(tmp_args_cnd_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),3)
                                 ])


    #--------------------------
    #GenVectorD_10:针对包含更精细的实参分析的原始数据文件
    #特征向量提取:4维
    #       callee实参参与的条件语句在Callsite存在的频率(即计算出现过Callsite的比率)
    #       callee实参共同参与的运算语句在Callsite存在的频率(左侧,右侧必须各有一个实参相关的symbol,直接相关)
    #       callee实参共同参与的条件语句在Callsite存在的频率
    #向量是否归一化:否
    #--------------------------
    def GenVectorD_10(self,filename):
        # 将callsite的各参数对应的度量值累加,参数之间存在重复的度量也多次计算;对一个call,将callsites的度量取平均值

        objfile = ObjDataAndBinFile()
        dbcalls = DataStruct_D.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)
        callinfo =[]

        for call in dbcalls.callinfolist:
            tmp_call_cnd_num = 0
            tmp_args_stmtsleft_num = 0
            tmp_args_stmtsright_num = 0
            tmp_args_stmtscall_num = 0
            tmp_args_cnd_num = 0
            tmp_args_coleaves_num = 0
            tmp_args_cocnds_num = 0
            tmp_args_cocnds_list = []



            for callsite in call.callsiteinfolist:
                flag_args_stmtsleft = False
                flag_args_stmtsright = False
                flag_args_stmtscall = False
                flag_args_cnd = False
                flag_coleaves = False
                flag_args_cocnds = False
                if(len(callsite.callsite_conditionslist) > 0):
                    tmp_call_cnd_num += 1
                for arginfo in callsite.callsite_argsinfolist:
                    if (len(arginfo.arg_stmtsleftlist) >= 1):
                        flag_args_stmtsleft = True
                    if (len(arginfo.arg_stmtsrightlist) >= 1):
                        flag_args_stmtsright = True
                    if (len(arginfo.arg_stmtiscalllist) >= 1):
                        flag_args_stmtscall = True
                    if (len(arginfo.arg_condidlist) >= 1):
                        flag_args_cnd= True

                if(flag_args_stmtsleft):
                    tmp_args_stmtsleft_num +=1
                if(flag_args_stmtsright):
                    tmp_args_stmtsright_num +=1
                if(flag_args_stmtscall):
                    tmp_args_stmtscall_num +=1
                if(flag_args_cnd):
                    tmp_args_cnd_num +=1


                for i in range(0,len(callsite.callsite_argsinfolist)):
                    for j in range(i+1,len(callsite.callsite_argsinfolist)):
                        for val_leaf in callsite.callsite_argsinfolist[i].arg_stmtsleftlist:
                             if val_leaf in callsite.callsite_argsinfolist[j].arg_stmtsrightlist:
                                flag_coleaves = True
                        #如果处于共同的call中,也视为相互定义
                        for val_call in callsite.callsite_argsinfolist[i].arg_stmtiscalllist:
                             if val_call in callsite.callsite_argsinfolist[j].arg_stmtiscalllist:
                                flag_coleaves = True


                        for val_cnd in callsite.callsite_argsinfolist[i].arg_condidlist:
                            if val_cnd in callsite.callsite_argsinfolist[j].arg_condidlist:
                                flag_args_cocnds = True

                if(flag_coleaves):
                    tmp_args_coleaves_num +=1
                    flag_coleaves = False
                if(flag_args_cocnds):
                    tmp_args_cocnds_num +=1
                    flag_args_cocnds = False

            #有些类的内部的函数,没能正确获取相关数据,占少数,比例,如370:6596
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 tmp_call_cnd_num,
                                 tmp_args_stmtsleft_num ,
                                 tmp_args_stmtsright_num ,
                                 tmp_args_stmtscall_num ,
                                 tmp_args_cnd_num ,
                                 tmp_args_coleaves_num ,
                                 tmp_args_cocnds_num
                                 ])
            '''
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 1 if tmp_args_cnd_num > call.callsiteNums/2 else 0,
                                 1 if tmp_args_coleaves_num > call.callsiteNums/2 else 0,
                                 1 if tmp_args_cocnds_num > call.callsiteNums/2 else 0
                                 ])
            '''
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_call_cnd_num/float(call.callsiteNums),3),
                                 round(tmp_args_stmtsleft_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_stmtsright_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_stmtscall_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cnd_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),3)
                                 ])
            '''
            if (call.callsiteNums != 0):
                callinfo.append([call.call_id,
                                 call.call_code,
                                 call.callsiteNums,
                                 round(tmp_args_cnd_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_coleaves_num/float(call.callsiteNums),3) ,
                                 round(tmp_args_cocnds_num/float(call.callsiteNums),3)
                                 ])

        return callinfo
if __name__ == '__main__':

    #import sys
    #apiFunc = sys.argv[1]
    ##filename = '../Data/Converted_opsData_20160628-180757.data'
    filename = '../Data/ConvertedOutData_Detail_20160712-222006.data'
    Cluster = xPoint()
    k =8
    Cluster.run(filename,k)
    print "Game over!\n"


