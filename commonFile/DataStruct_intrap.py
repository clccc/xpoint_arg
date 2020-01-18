#coding:utf-8
#code by Chenlin 2016-03-26
#功能: 过程内的实参信息相关结构体.

#callee的实参基本信息
#arg_id: 代码属性图中本实参的id
#arg_code:实参代码
#arg_condidlist:实参参与的条件语句的id列表
#arg_stmtsleftlist:实参作为左值的语句id列表
#arg_stmtsrightlist:实参作为右值的语句id列表
#arg_stmtiscalllist:实参作为参数的函数被使用的语句id列表.
class ArgInfo:
    def __init__(self, id, code, symbolset, definestatments, defvar):
        self.id = id
        self.code = code
        self.symbolset = symbolset
        self.definestatments = definestatments
        self.defvar = defvar

#callee的基本信息
# callsite_id : 在代码属性图中的此callee所在语句的id
# callsite_code: 本callee的调用点处的语句
# callsite_conditionslist: 与本callee相关的条件语句列表
# callsite_argsinfolist: callee的实参信息列表,为ArgInfo结构的列表
class CallSiteInfo:
    def __init__(self, id, code, argcheckresult, cndlistbycontrol, conditionslist, argsinfolist):
        self.call_id = id
        self.call_code = code
        self.argcheckresult = argcheckresult
        self.cndlistbycontrol = cndlistbycontrol
        self.cndlistincfgpathNOcontrol = conditionslist
        self.argsinfolist = argsinfolist

#被调用函数的基本信息:
# call_id 在代码属性图中的id号
# call_code函数名
# callsiteNums 被调用次数
# callsiteinfolist 具体调用信息列表,是CallSiteInfo结构列表
class CallInfo:
    def __init__(self, id, code, callsiteNums, callsiteinfolist):
        self.call_id = id
        self.call_code = code
        self.callsiteNums = callsiteNums
        self.callsiteinfolist = callsiteinfolist

#所有被调用过的函数的列表,包括有函数体的和无函数体的外部函数. 没有被调用过的函数不在此列.
# callinfolist 被调用函数的基本信息列表,CallInfo结构的列表
class DbCalls:
    def __init__(self):
        self.numofcalls = 0 # 被调用函数的数量
        self.callinfolist = []