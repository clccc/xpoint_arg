#coding:utf-8
#code by Chenlin 2016-03-26
#参数定义符号上溯多层
class ArgInfo:
    def __init__(self, id, code, condidlist, stmtsleftlist, stmtsrightlist, stmtiscalllist):
        self.arg_id = id
        self.arg_code = code
        self.arg_condidlist = condidlist
        self.arg_stmtsleftlist = stmtsleftlist
        self.arg_stmtsrightlist = stmtsrightlist
        self.arg_stmtiscalllist = stmtiscalllist

class CallSiteInfo:
    def __init__(self, id, code, conditionslist, argsinfolist):
        self.callsite_id = id
        self.callsite_code = code
        self.callsite_conditionslist = conditionslist
        self.callsite_argsinfolist = argsinfolist


class CallInfo:
    def __init__(self, id, code, callsiteNums, callsiteinfolist):
        self.call_id = id
        self.call_code = code
        self.callsiteNums = callsiteNums
        self.callsiteinfolist = callsiteinfolist


class DbCalls:
    def __init__(self):
        self.numofcalls = 0
        self.callinfolist = []