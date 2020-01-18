//by cl
//2016-06-30 08:51:31

class CallInfo_intrap{
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
class CallsiteInfo_intrap{
    def callsiteid;
    def callsitecode;
    def argcheckresult = []; //对参数的检查情况
    def cndlistbycontrol =[]; //对本函数调用的控制依赖链构成的条件语句id集合,元素顺序为最内层条件依次延伸到最外层
    def cndlistincfgpathNOcontrol = []; //与本函数调用相关的CFG路径上的条件语句id集合,去除存在控制依赖的节点.
    def argsinfolist = []
}

/**
 *
 * 具体函数调用的外部调用前的实参相关的预操作信息
 * - 实参id
 * - 实参code
 * - 通过in('label',"REACHES")传达到实参的最外层节点id构成的集合.
**/
class ArgInfo_intrap{
    def argid;
    def argcode;
    def symbolset = []
    def definestatments = [] //通过REACHES边回溯的节点集.
    def defvar = []
}
