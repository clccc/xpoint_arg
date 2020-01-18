#coding:utf-8
#-----------------------------
#code by Chenlin
#-----------------------------

import sys
sys.path.append("..")
import commonFile.DataStruct as DataStruct
import commonFile.DataStruct_D as DataStruct_D
import commonFile.DataStruct_M as DataStruct_M
import commonFile.DataStruct_intrap as DataStruct_intrap
import commonFile.OPS_DataStruct as OPS_DataStruct
from py2neo.packages.httpstream import http

from DBContentsProvider import DBContentsProvider

http.socket_timeout = 999999


class GetCodesStatsData():
    def __init__(self, name_project):
        self.contentprovider = DBContentsProvider()
        self.name_project = name_project

    '''
    def GetStatsData(self):
        query = "getCallsInfoList()"
        callsinfolist = self.contentprovider.RunGremlinQuery(query)
        return callsinfolist

    def GetOutStatsData(self):
        query = "getCallOpsInfoList()"
        callOpsinfolist = self.contentprovider.RunGremlinQuery(query)

        filename = "../Data/OutStatsData_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        print "生成GetOutStatsData的原始数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(callOpsinfolist,filename)

        return callOpsinfolist

    def GetOutStatsData_Detail(self):
        query = "getCallOpsInfoList_D()"
        callOpsinfolist = self.contentprovider.RunGremlinQuery(query)

        filename = "../Data/OutStatsData_D_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        print "生成GetOutStatsData_Detail的原始数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(callOpsinfolist,filename)

        return callOpsinfolist

    def GetOutStatsData_Mutil(self):
        query = "getCallOpsInfoList_M()"
        callOpsinfolist = self.contentprovider.RunGremlinQuery(query)

        filename = "../Data/OutStatsData_M_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        print "生成GetOutStatsData_Mutil的原始数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(callOpsinfolist,filename)

        return callOpsinfolist
    '''
    def GetOutStatsData_intrap(self):
        query = "getCallOpsInfoList_intrap()"
        #query = "test()"
        callOpsinfolist = self.contentprovider.RunGremlinQuery(query)

        #filename = "../Data/intrap_OutStatsData_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        #print "生成GetOutStatsData_intrap的原始数据文件:%s"%filename
        #objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        #objfile.objdata2file(callOpsinfolist,filename)

        return callOpsinfolist

    def GetOutStatsData_intrap_samples(self):
        query = "getCallOpsInfoList_intrap_samples()"
        #query = "test()"
        callOpsinfolist = self.contentprovider.RunGremlinQuery(query)

        #filename = "../Data/intrap_OutStatsData_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        #print "生成GetOutStatsData_intrap的原始数据文件:%s"%filename
        #objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        #objfile.objdata2file(callOpsinfolist,filename)

        return callOpsinfolist


    '''
    def ConvertData(self,callsinfolist):
        dbcalls = DataStruct.DbCalls()
        dbcalls.numofcalls = len(callsinfolist)
        dbcalls.callinfolist = [DataStruct.CallInfo(a[0], a[1], a[2], [
            DataStruct.CallSiteInfo(b[0], b[1], b[2], [
                DataStruct.ArgInfo(*c) for c in b[3]
                ]) for b in a[3]
            ]) for a in callsinfolist]
        return dbcalls

    def ConvertOutData(self,callsopsinfolist):
        dbcalls = OPS_DataStruct.DbCalls()
        dbcalls.numofcalls = len(callsopsinfolist)
        dbcalls.callinfolist = [OPS_DataStruct.CallInfo(a[0], a[1], a[2], [
            OPS_DataStruct.CallSiteInfo(b[0], b[1], b[2], [
                OPS_DataStruct.ArgInfo(*c) for c in b[3]
                ]) for b in a[3]
            ]) for a in callsopsinfolist]

        filename = "../Data/ConvertedOutData_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        print "生成ConvertOutData转换后的数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(dbcalls,filename)

        return dbcalls

    def ConvertOutData_Detail(self,callsopsinfolist):
        dbcalls = DataStruct_D.DbCalls()
        dbcalls.numofcalls = len(callsopsinfolist)
        dbcalls.callinfolist = [DataStruct_D.CallInfo(a[0], a[1], a[2], [
            DataStruct_D.CallSiteInfo(b[0], b[1], b[2], [
                DataStruct_D.ArgInfo(*c) for c in b[3]
                ]) for b in a[3]
            ]) for a in callsopsinfolist]

        filename = "../Data/ConvertedOutData_Detail_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        print "生成ConvertOutData_Detail转换后的数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(dbcalls,filename)

        return dbcalls

    def ConvertOutData_Mutil(self,callsopsinfolist):
        dbcalls = DataStruct_M.DbCalls()
        dbcalls.numofcalls = len(callsopsinfolist)
        dbcalls.callinfolist = [DataStruct_M.CallInfo(a[0], a[1], a[2], [
            DataStruct_M.CallSiteInfo(b[0], b[1], b[2], [
                DataStruct_M.ArgInfo(*c) for c in b[3]
                ]) for b in a[3]
            ]) for a in callsopsinfolist]

        filename = "../Data/ConvertedOutData_Mutil_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        print "生成ConvertOutData_Mutil转换后的数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(dbcalls,filename)

        return dbcalls
    '''
    def ConvertOutData_intrap(self,callsopsinfolist):
        dbcalls = DataStruct_intrap.DbCalls()
        dbcalls.numofcalls = len(callsopsinfolist)
        dbcalls.callinfolist = [DataStruct_intrap.CallInfo(a[0], a[1], a[2], [
            DataStruct_intrap.CallSiteInfo(b[0], b[1], b[2], b[3], b[4], [
                DataStruct_intrap.ArgInfo(*c) for c in b[5]
                ]) for b in a[3]
            ]) for a in callsopsinfolist]

        filename = "../Data/%s-xpoint_arg.data"%self.name_project
        print "生成xpoint_arg的特征数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(dbcalls,filename)

        return dbcalls
    '''
    def ConvertOutData_Detail_FromFile(self,filename):
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        callsopsinfolist= objfile.binfile2objdata(filename)
        dbcalls = DataStruct_D.DbCalls()
        dbcalls.numofcalls = len(callsopsinfolist)
        dbcalls.callinfolist = [DataStruct_D.CallInfo(a[0], a[1], a[2], [
            DataStruct_D.CallSiteInfo(b[0], b[1], b[2], [
                DataStruct_D.ArgInfo(*c) for c in b[3]
                ]) for b in a[3]
            ]) for a in callsopsinfolist]

        filename = "../Data/ConvertedOutData_Detail_%s.data"%time.strftime('%Y%m%d-%H%M%S')
        print "生成ConvertOutData_Detail转换后的数据文件:%s"%filename
        objfile = ObjDataAndBinFile.ObjDataAndBinFile()
        objfile.objdata2file(dbcalls,filename)

        return dbcalls
    '''

    '''
    def run(self):
        callsinfolist = self.GetStatsData()
        cbStatsData = self.ConvertData(callsinfolist)
        return cbStatsData

    def run_out(self):
        callsopsinfolist = self.GetOutStatsData()
        cbStatsData = self.ConvertOutData(callsopsinfolist)
        return cbStatsData

    def run_out_detail(self):
        callsopsinfolist = self.GetOutStatsData_Detail()
        cbStatsData = self.ConvertOutData_Detail(callsopsinfolist)
        return cbStatsData

    def run_out_mutil(self):
        callsopsinfolist = self.GetOutStatsData_Mutil()
        cbStatsData = self.ConvertOutData_Mutil(callsopsinfolist)
        return cbStatsData
    '''
    def run_out_intrap(self):
        callsopsinfolist = self.GetOutStatsData_intrap()
        cbStatsData = self.ConvertOutData_intrap(callsopsinfolist)
        return cbStatsData

    def run_out_intrap_samples(self):
        callsopsinfolist = self.GetOutStatsData_intrap_samples()
        cbStatsData = self.ConvertOutData_intrap(callsopsinfolist)
        return cbStatsData

    '''
    def run_out_detail_fromfile(self,filename):
        cbStatsData = self.ConvertOutData_Detail_FromFile(filename)
        return cbStatsData
    '''



if __name__ == '__main__':

    import datetime
    import time
    from commonFile import ObjDataAndBinFile

    starttime = datetime.datetime.now()
    print ("\nBegin: %s")%starttime
    name_project = sys.argv[1] # 输入项目名称，用于中间结果的文件名
    gen = GetCodesStatsData(name_project)
    #dbcalls = gen.run()
    #gen.run_out()
    #gen.run_out_detail()
    #gen.run_out_mutil()

    #获取所有 函数
    #gen.run_out_intrap()
    #获取sammoles列表的函数
    gen.run_out_intrap_samples()

    #filename = '../Data/intrap_OutStatsData_20191026-142106.data'
    #filename = '../Data/intrap_ConvertedOutData_20191026-142106.data'
    #gen.run_out_detail_fromfile(filename)
    endtime = datetime.datetime.now()
    print ("\nEnd: %s")%endtime
    print ("\nTime Used: %s")%(endtime - starttime)

    #werw = []
    #werw = objfile.binfile2objdata(filename)
    print "ok"


