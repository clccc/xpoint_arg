#code by Chenlin 2016-03-26
#coding:utf-8

import DataStruct

import plot
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
        callinfo =[]

        args_leaves_num = []
        args_cnd_num = []
        tmp_args_leaves_num = 0
        tmp_args_cnd_num = 0
        for call in dbcalls.callinfolist:
            tmp_args_leaves_num = 0
            tmp_args_cnd_num = 0
            for callsite in call.callsiteinfolist:
                for arginfo in callsite.callsite_argsinfolist:
                        if arginfo.arg_leavesNumsInThisCall > tmp_args_leaves_num:
                            tmp_args_leaves_num = arginfo.arg_leavesNumsInThisCall
                        if arginfo.arg_condNumsInThisCall > tmp_args_cnd_num:
                            tmp_args_cnd_num = arginfo.arg_condNumsInThisCall

            args_leaves_num.append(tmp_args_leaves_num)
            args_cnd_num.append(tmp_args_cnd_num)

            callinfo.append([call.call_id,str(call.call_code),tmp_args_leaves_num,tmp_args_cnd_num])
            #print call.call_code , u":" , args_leaves_num , u"-" , args_cnd_num


        myplot = plot.plot()
        #myplot.plot(args_leaves_num,args_cnd_num,'max-2d.png')

        x = range(1,len(callinfo)+1)
        myplot.plot3d(x,args_leaves_num,args_cnd_num,'max-3d.png')


        callinfos =sorted(callinfo, key=lambda a : a[2])

        

        f = open('openssl101f-max.txt','w')
        for callinfo in callinfos:
            f.write(str(callinfo[0])+str(" _ ")+str(callinfo[1])+str(":")+str(callinfo[2])+str("-")+str(callinfo[3]))
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


