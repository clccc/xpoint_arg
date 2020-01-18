#code by Chenlin 2016-03-26
#coding:utf-8

from __future__ import division

import DataStruct

from commonFile.ObjDataAndBinFile import ObjDataAndBinFile


class   xPoint:
    def run(self,filename):
        """"
        每类对象的x矢量：
            对象实例的预处理力度 pDealIntensity_calleeg.
            对象的预处理力度均值
            对象的实例个数／代码量总函数实例个数
            参数敏感度
            对象对参数的内处理力度
        """

        objfile = ObjDataAndBinFile()
        dbcalls = DataStruct.DbCalls()
        dbcalls = objfile.binfile2objdata(filename)

        callsinfo =[]
        for call in dbcalls.callinfolist:
            num_call_args =0
            avg_args_cnd =0
            avg_args_leaves = 0
            #获取call的参数个数，考虑参数个数可变的情况
            for callsite in call.callsiteinfolist:
                if callsite.callsite_argNums > num_call_args:
                     num_call_args= callsite.callsite_argNums

            # 以下代码可以替换为tmplist_arg_leaves = [[] for i in range(num_call_args)]
            tmplist_arg_leaves = [[]]* num_call_args
            tmplist_arg_cnd = [[]]*num_call_args
            for t in range(0,num_call_args):
                tmplist_arg_cnd[t] = []
                tmplist_arg_leaves[t] = []


            for callsite in call.callsiteinfolist:
                for i in range(0,callsite.callsite_argNums):
                    tmplist_arg_leaves[i].append(callsite.callsite_argsinfolist[i].arg_leavesNumsInThisCall)
                    tmplist_arg_cnd[i].append(callsite.callsite_argsinfolist[i].arg_condNumsInThisCall)

            argsinfo=[]
            for j in range(0,num_call_args):
                avg_args_cnd = sum(tmplist_arg_cnd[j])/len(tmplist_arg_cnd[j])
                avg_args_leaves = sum(tmplist_arg_leaves[j])/len(tmplist_arg_leaves[j])
                argsinfo.append([j,avg_args_leaves,avg_args_cnd])

            callsinfo.append([call.call_id, call.call_code,argsinfo])

        #print len(callsinfo)
        #print callsinfo



        """
        myplot = plot.plot()
        #myplot.plot(args_leaves_num,args_cnd_num)

        x = range(1,len(callinfo)+1)
        myplot.plot3d(x,args_leaves_num,args_cnd_num)


        callinfos =sorted(callinfo, key=lambda a : a[2])
        """
        f = open('openssl101f-avg.txt','w')
        for callinfo in callsinfo:
            f.write(str(callinfo[0])+str(" _ ")+str(callinfo[1])+str(":")+str(callinfo[2]))
            f.write('\n')
        f.close()
            #print "\n"

        print 'run() End'
if __name__ == '__main__':

    #import sys
    #apiFunc = sys.argv[1]
    filename = "openssl.data"
    tool = xPoint()
    tool.run(filename)
    print "Game over!\n"


