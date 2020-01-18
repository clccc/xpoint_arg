#code by Chenlin 2016-03-26

class ArgInfo:
    def __init__(self, id, code, leavesIdlist, condIdlist):
        self.arg_id = id
        self.arg_code = code
        self.arg_leavesIdlist = leavesIdlist
        self.arg_condIds = condIdlist


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