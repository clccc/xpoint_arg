//by cl
//2016-06-30 08:51:31

class CallInfo{
    def id;
    def code;
    def callsiteNums = 0;
    def callsiteinfolist = []
}

/**
 *
 * 具体函数调用的外部调用前的预操作信息
 * - callexpression的id
 * - callexpression的code
 * - 调用前，各个实参的相关预操作信息构成的列表
 * - 调用前，需满足的条件语句id列表
 **/
class CallsiteInfo{
    def callsiteid;
    def callsitecode;
    def conditionslist =[];
    def argsinfolist = []
}

/**
 *
 * 具体函数调用的外部调用前的实参相关的预操作信息
 * - 实参id
 * - 实参code
 * - 调用前，参与的运算语句id列表（算式左侧即被修改，所有有实参参与的函数语句作为左侧类型的运算加入）
 * - 调用前，参与的运算语句id列表（算式右侧）
 * - 调用前，参与需满足条件语句列表
 **/
class ArgInfo_D{
    def argid;
    def argcode;
    def conditionslist =[]
    def stmtsleftlist = []
    def stmtsrightlist = []
    def stmtiscalllist = []

}

class ArgInfo_S{
    def argid;
    def argcode;
    //def stmtsleftlist = []
    //def stmtsrightlist = []
    def statementslist = []
    def conditionslist =[]
}

/**
 * 函数的内部实现相关的统计信息
 * - call的id
 * - 各个形参参与的运算语句id列表
 * - 代码行数
 * - 内部调用函数的id列表
 * - 函数的路径数
 * - 有没有内存操作
 * - 有没有用户数据参与
 **/
class FuncOpsGraph{
    def funcid;
    def paramsinfo = []
    //def numoflines
    //def containscallsiteids =[]
    //def numofpaths
    //def hasmemop
    //def hasuserdata
    //def callsiteOpsGraphlist = []
}
