//by cl 2017-03-13 10:47:28
/*
功能: 获取被调用函数实参的相关信息,为参数检查的分析提供基础素材. 本分支只考虑过程内的实参信息,即caller对callee的实参处理不考虑
上层caller对本层caller的实参的处理而影响到callee实参检查的情况.当本层caller对callee参数没有检查时可能需要递归上溯,此情况待后续分析,
不包含在本代码文件中.
符号说明:_intrap 表示过程内分析
*/


/*
功能:根据一个CFG节点递归获取与其变量直接和间接相关的所有定义语句id
注意:有没有循环的问题?
*/
Object.metaClass.getdefineStmtsofcfgnode = { cfgnodeid ->
    //println "In - getdefineStmtsofcfgnode(" +  cfgnodeid  + ")"
    def definestmts_intrap=[]
    def definenode_traversed = [] //保存已经访问过的定义语句节点,防止递归循环
    def definestmtlist= g.v(cfgnodeid).in('label','REACHES').id.toList()
    for(;definestmtlist;){
        nodeid = definestmtlist[0]
        definestmtlist.remove(nodeid)//从待处理列表中删除
        if(definenode_traversed.contains(nodeid)){//如果该节点已经访问过,不再处理.
            continue;
        }
        definenode_traversed.add(nodeid)//标记该节点为已访问
        definestmts_intrap.add(nodeid)
        tmplist = g.v(nodeid).in('label','REACHES').id.toList()
        tmplist.removeAll(definenode_traversed)//去除已遍历的
        tmplist.removeAll(definestmtlist)//去除已加入待处理列表的
        definestmtlist.addAll(tmplist)//将新节点加入待处理列表
    }
    return definestmts_intrap;
}


/*
功能:根据一个(CFG节点id,define var)递归获取与其变量直接和间接相关的所有定义语句id
注意:definestmt's REACHES-var set has little difference with the USE symbols set.
*/
Object.metaClass.getdefineStmtsbyidAndvar = { cfgnodeid,var ->
    //println "In - getdefineStmtsofcfgnode(" +  cfgnodeid  + ")"
    def definestmts_intrap=[]
    def definenode_traversed = [] //保存已经访问过的定义语句节点,防止递归循环
    def definestmtlist= g.v(cfgnodeid).inE('label','REACHES').has('var',var).outV.id.toList()


    for(;definestmtlist;){
        nodeid = definestmtlist[0]
        definestmtlist.remove(nodeid)//从待处理列表中删除
        if(definenode_traversed.contains(nodeid)){//如果该节点已经访问过,不再处理.
            continue;
        }
        definenode_traversed.add(nodeid)//标记该节点为已访问
        definestmts_intrap.add(nodeid)
        tmplist = g.v(nodeid).in('label','REACHES').id.toList()
        tmplist.removeAll(definenode_traversed)//去除已遍历的
        tmplist.removeAll(definestmtlist)//去除已加入待处理列表的
        definestmtlist.addAll(tmplist)//将新节点加入待处理列表
    }
    return definestmts_intrap;
}

/*获取节点symbol集
*/
Object.metaClass.getsymbolset = {id ->
    symbolset=g.v(id).out('label','USE').code.toList()
    return symbolset;
}


/*获取CFG节点的定义链中变量集,可能存在重复元素
*/
Object.metaClass.getdefvar = {cfgnodeid ->
    def result=[]
    def definenode_traversed = [] //保存已经访问过的定义语句节点,防止递归循环
    def definestmtlist= g.v(cfgnodeid).in('label','REACHES').id.toList()
    def var_list = g.v(cfgnodeid).inE('label','REACHES').var.toList()
    result.addAll(var_list)
    for(;definestmtlist;){
        nodeid = definestmtlist[0]
        definestmtlist.remove(nodeid)//从待处理列表中删除
        if(definenode_traversed.contains(nodeid)){//如果该节点已经访问过,不再处理.
            continue;
        }
        definenode_traversed.add(nodeid)//标记该节点为已访问
        var_list = g.v(nodeid).inE('label','REACHES').var.toList()
        result.addAll(var_list)
        tmplist = g.v(nodeid).in('label','REACHES').id.toList()
        tmplist.removeAll(definenode_traversed)//去除已遍历的
        tmplist.removeAll(definestmtlist)//去除已加入待处理列表的
        definestmtlist.addAll(tmplist)//将新节点加入待处理列表
    }
    return result;
}

/*获取CFG节点的定义链中(语句,变量)元组集,可能存在重复元素
*/
Object.metaClass.getdefidandvar = {cfgnodeid ->

}


/*
功能:根据一个(CFG节点id,define var)递归获取与其变量直接和间接相关的所有定义语句的var集
注意:definestmt's REACHES-var set has little difference with the USE symbols set.
*/
Object.metaClass.getdefvarbyidAndvar = { cfgnodeid,var ->
    //println "In - getdefvarbyidAndvar(" +  cfgnodeid + "," + var  + ")"
    def defvar=[]
    def definenode_traversed = [] //保存已经访问过的定义语句节点,防止递归循环
    def definestmtlist= g.v(cfgnodeid).inE('label','REACHES').has('var',var).outV.id.toList()
    defvar.add(var)
    for(;definestmtlist;){
        nodeid = definestmtlist[0]
        definestmtlist.remove(nodeid)//从待处理列表中删除
        if(definenode_traversed.contains(nodeid)){//如果该节点已经访问过,不再处理.
            continue;
        }
        definenode_traversed.add(nodeid)//标记该节点为已访问
        var_list = []
        var_list = g.v(nodeid).inE('label','REACHES').var.toList()
        defvar.addAll(var_list)
        tmplist = g.v(nodeid).in('label','REACHES').id.toList()
        tmplist.removeAll(definenode_traversed)//去除已遍历的
        tmplist.removeAll(definestmtlist)//去除已加入待处理列表的
        definestmtlist.addAll(tmplist)//将新节点加入待处理列表
    }
    return defvar;
}

/*
功能:根据一个CFG节点获取它的前置控制依赖的条件id列表
注意:有没有循环的问题?存在,首先在openssl源码中有大量的goto语句,显然一些代码库中,goto的使用是较为常见的,另外while,for循环也会导致控制循环.
*/

Object.metaClass.getCndlistbycontrol_intrap = { cfgnodeid ->
    //println "In getCndlistbycontrol_intrap(" + cfgnodeid + ")"
    def cndlistbycontrol_intrap=[] //前置控制依赖条件语句列表
    def cndlistbycontrol_traversed=[] //标记已访问过的节点
    def cfgnodelist= g.v(cfgnodeid).in('label','CONTROLS').id.toList()
    //多个直接控制条件语句
    for(;cfgnodelist.size()>0;){
        nodeid=cfgnodelist[0]
        cfgnodelist.remove(nodeid)//从待处理列表中删除
        if(cndlistbycontrol_traversed.contains(nodeid)){//如果该节点已经访问过,不再处理.
            continue;
        }
        cndlistbycontrol_traversed.add(nodeid)//标记该节点为已访问
        if(g.v(nodeid).code == "ENTRY"){
            continue;
        }
        cndlistbycontrol_intrap.add(nodeid)
        tmplist = g.v(nodeid).in('label','CONTROLS').id.toList()
        tmplist.removeAll(cndlistbycontrol_traversed)//去除已遍历的
        tmplist.removeAll(cfgnodelist)//去除已加入待处理列表的
        cfgnodelist.addAll(tmplist)//将新节点加入待处理列表
    }
    return cndlistbycontrol_intrap;


    /*
    //注意: 不考虑类似goto的代码,可以假定每个CFG节点的直接控制条件语句只会有一个,并且每个CFG节点至少有一个控制依赖节点ENTRY,故不考虑null的情况.
    def controlID = g.v(cfgnodeid).in('label','CONTROLS').id.toList()[0]
    //println controlID
    if(g.v(controlID).code != "ENTRY"){
        cndlistbycontrol_intrap.add(controlID)
        getCndlistbycontrol_intrap(controlID)
    }
    return cndlistbycontrol_intrap;
    */
}

/*
功能:根据一个CFG节点获取它的前置CFG路径上的条件id列表cndlistincfgpath
注意:如何处理CFG图的循环?
*/

//非递归
Object.metaClass.getCndlistfromcfgpath_intrap = { cfgnodeid ->
    //println "In getCndlistfromcfgpath_intrap(" + cfgnodeid + ")"
    def cndlistfromcfgpath_intrap=[]
    def cfgnode_traversed = [] //保存已经访问过的CFG节点,防止递归循环
    def cfgnodelist= g.v(cfgnodeid).in('label','FLOWS_TO').id.toList()
    for(;cfgnodelist.size()>0;){
        //println cfgnodelist
        nodeid=cfgnodelist[0]
        cfgnodelist.remove(nodeid)//从待处理列表中删除
        if(cfgnode_traversed.contains(nodeid)){//如果该节点已经访问过,不再处理.
            continue;
        }
        cfgnode_traversed.add(nodeid)//标记该节点为已访问
        if(g.v(nodeid).type == "Condition"){
            cndlistfromcfgpath_intrap.add(nodeid)
        }
        if(g.v(nodeid).code == "ENTRY"){
            continue;
        }
        else {
            tmplist = g.v(nodeid).in('label','FLOWS_TO').id.toList()
            tmplist.removeAll(cfgnode_traversed)//去除已遍历的
            tmplist.removeAll(cfgnodelist)//去除已加入待处理列表的
            cfgnodelist.addAll(tmplist)//将新节点加入待处理列表
        }
    }
    return cndlistfromcfgpath_intrap;
}

/*** 递归版本的图遍历6213
Object.metaClass.getCndlistfromcfgpath_intrap = { cfgnodeid ->
    //println "In getCndlistfromcfgpath_intrap(" + cfgnodeid + ")"

    if(cfgnode_traversed.contains(cfgnodeid)){//如果该节点已经访问过,不再处理.
        return cndlistfromcfgpath_intrap;
    }
    else{
        cfgnode_traversed.add(cfgnodeid)//标记该节点为已访问
    }
    def cfgnodelist= g.v(cfgnodeid).in('label','FLOWS_TO').id.toList()
    for(nodeid in cfgnodelist){
        if(g.v(nodeid).code == "ENTRY"){
            continue;
        }
        else {
            if(g.v(nodeid).type == "Condition"){
                cndlistfromcfgpath_intrap.add(nodeid)
            }
        getCndlistfromcfgpath_intrap(nodeid)
        }
    }
    return cndlistfromcfgpath_intrap;
}
***/

//判断一个id是否为CFGNode,并且是一个函数
Object.metaClass.IsCFGNodeACall = { cfgnodeid ->
    if(g.v(cfgnodeid).isCFGNode == "True")
    {
        if(g.v(cfgnodeid).outE('IS_AST_intrapARENT').inV.has('type','CallExpression').toList().code.contains(g.v(cfgnodeid).code))
            return true;
        else
            return false;
    }
    return false
}

Object.metaClass.IsDefined = { symbolid,statementid ->
    if(g.v(statementid).outE("DEF").inV.toList().id.toString().contains(symbolid.toString()))
    {
        return true;
    }
    else
        return false
}

/**
 Create a CallsiteInfo:
 问题:1. //此处有且一项,ExpressionStatement
    def cfgnodeid = g.v(callsiteid)._().statements().id.toList().toList()[0]
    中获取为null的后面的语句和条件列表直接置为空,但实际存在出入.
    2. callsite调用的前置控制依赖条件集和实参参与的条件集不是包含与被包含的关系,是否需要整理?需要!
    非控制依赖的条件语句,需要判断其对参数的定义变量集合的一个或多个元素进行了检查.
**/
Object.metaClass.createCallsiteInfo_intrap = { callsiteid ->
    //println "\n* createCallsiteInfo_intrap(CallSiteID =  " + callsiteid +")"
    def CallsiteInfo = new CallsiteInfo_intrap();

    /*1. 获取callsite的id和code*/
    CallsiteInfo.callsiteid = callsiteid;
    CallsiteInfo.callsitecode = g.v(callsiteid).code;
    argSet = g.v(callsiteid)._().callToArguments().id.toList() //.sort()

    //println "\t1. callsite的基本信息:"
    //println "\t\tID = " + CallsiteInfo.callsiteid + " ; CODE = " + CallsiteInfo.callsitecode

     /*2. 获取callsite的前置控制依赖的条件列表*/

    //获取callsite对应的CFG类型的节点,此处有且一项,ExpressionStatement . 2017-02-18 22:05:55 此为假设,待考虑?

    def cfgnodeid = g.v(callsiteid)._().statements().id.toList().toList()[0] //2017-02-18 22:04:43 此处[0]是否简化了情况,待考虑?
    if(cfgnodeid == null){
        println "error"
        CallsiteInfo.cndlistbycontrol = []
        CallsiteInfo.argsinfolist = []
        CallsiteInfo.argcheckresult = "错误:无结果"
        CallsiteInfo.cndlistincfgpathNOcontrol = []
        return CallsiteInfo;
    }
    else{
        //注意此处getCndlistbycontrol_intrap返回的是list,所以要用addAll,而不是add

        CallsiteInfo.cndlistbycontrol.addAll(getCndlistbycontrol_intrap(cfgnodeid))
    }
    //println "\t2. callsite(CFG_ID=" + cfgnodeid + ")的前置控制依赖的条件: "
    //println "\t\t" + CallsiteInfo.cndlistbycontrol

    /*3. 获取callsite的数据流路径上的条件列表,并去除与cndlistbycontrol_intrap重复的条件节点.*/
    CallsiteInfo.cndlistincfgpathNOcontrol.addAll(getCndlistfromcfgpath_intrap(cfgnodeid))
    CallsiteInfo.cndlistincfgpathNOcontrol.removeAll(CallsiteInfo.cndlistbycontrol)
    //println "\t3. callsite的前置非控制条件: "
    //println "\t\t" + CallsiteInfo.cndlistincfgpathNOcontrol

    /*4. 获取实参预操作信息*/
    //println "\t4. 实参预信息 "
    argset_varandsymbol_list =[]
    i = 0
    for(argid in argSet){ // 参数挨个处理
        def argInfo = new ArgInfo_intrap()
        argInfo.argid = argid
        argInfo.argcode = g.v(argid).code
        //将REACHES边的var属性和参数的use出边的symbol对应以归类. 按参数将定义语句分类
        symbolset=g.v(argid).out('label','USE').code.toList()
        argInfo.symbolset.addAll(symbolset)
        for(symbol in symbolset){
            argInfo.definestatments.addAll(getdefineStmtsbyidAndvar(cfgnodeid,symbol))
            argInfo.defvar.addAll(getdefvarbyidAndvar(cfgnodeid,symbol))
        }
        CallsiteInfo.argsinfolist.add(argInfo)
        //将参数的defvar集和symbol集合归并到一个集合中,在后续检查中使用
        tmplist = []
        tmplist.addAll(CallsiteInfo.argsinfolist[i].symbolset)
        tmplist.addAll(CallsiteInfo.argsinfolist[i].defvar)
        argset_varandsymbol_list.add(tmplist)
        i = i+1
        //println "\t\t*argID = " + argInfo.argid + " ; CODE = " + argInfo.argcode
        //println "\t\t symbols = " + argInfo.symbolset  + " ; defstmts = " + argInfo.definestatments + "; defvar = " +argInfo.defvar
    }

    /*5. 获取参数调用检查的结果argcheckresult
        CallsiteInfo.argcheckresult = "jointcheck"
        CallsiteInfo.argcheckresult = "单参数控制依赖上的检查"
        CallsiteInfo.argcheckresult = "单参数非控制条件上的检查"
        CallsiteInfo.argcheckresult = "无检查"
    */
    //println "\t5. 分析实参检查情况"
    //5-a. 共同的定义语句的参数检查. It must be compain-check when they have a same definestatment.

    //println "\t\t1. 共同定义语句的参数检查"
    num_args = CallsiteInfo.argsinfolist.size()
    for (i=0;i<num_args;i++){
        for (j=i+1;j<num_args;j++){
            tmp_dstmtlist = []
            tmp_dstmtlist.addAll(CallsiteInfo.argsinfolist[i].definestatments)
            tmp_dstmtlist.retainAll(CallsiteInfo.argsinfolist[j].definestatments)

            tmp_symbollist = []
            tmp_symbollist.addAll(CallsiteInfo.argsinfolist[i].symbolset)
            tmp_symbollist.retainAll(CallsiteInfo.argsinfolist[j].symbolset)
            if((tmp_dstmtlist.size()>0)||(tmp_symbollist.size()>0)) {
                if(i<j)
                    CallsiteInfo.argcheckresult.add("jointcheck-defstmt"+"(" + i + ","+ j+ ")")
                else
                    CallsiteInfo.argcheckresult.add("jointcheck-defstmt"+"(" + j + ","+ i+ ")")

                //println "\t[*] "+CallsiteInfo.argcheckresult
                //return CallsiteInfo
            }
        }
    }

    //5-b. 控制依赖条件下的参数检查
    //查看参数和控制依赖条件语句各自的defvar_symbol集之间是否有交集
    //println "\t\t2. 控制依赖条件下的参数检查 "

    for(cndctrl in CallsiteInfo.cndlistbycontrol){
        cnd_varandsymbol_list = []
        cnd_varandsymbol_list.addAll(getdefvar(cndctrl))
        cnd_varandsymbol_list.addAll(getsymbolset(cndctrl))
        for (i=0;i<num_args;i++){
            tmplist = []
            tmplist.addAll(argset_varandsymbol_list[i])
            tmplist.retainAll(cnd_varandsymbol_list)
            if(tmplist.size()>0){//参数a和依赖条件之间是否有共同的定义语句(说明条件语句中有参数参加)
                //CallsiteInfo.argcheckresult = "singlcheck-ctrlcnd"
                CallsiteInfo.argcheckresult.add("singlcheck-ctrlcnd"+"(" + i  +")")
                //追加检查:检查是否有其它参数b参加.此处可以允许b参数在条件结构体内再次定义(这被认为是检查的后续纠正操作),
                //为此不能通过检查参数b和条件是否有相同的定义语句,可以条件语句和b语句的symbol_var交集.
                for(j=0;j<num_args;j++){
                    if(j==i){//不和当前参数比较
                        continue;
                    }
                    else{
                        tmplist = []
                        tmplist.addAll(argset_varandsymbol_list[j])
                        tmplist.retainAll(cnd_varandsymbol_list)//求条件的symbol集与其它参数的symbol集的交集
                        if(tmplist.size()>0)
                        {
                            //CallsiteInfo.argcheckresult = "jointcheck-ctrlcnd"
                            if(i<j)
                                CallsiteInfo.argcheckresult.add("jointcheck-ctrlcnd"+"(" + i + ","+ j+ ")")
                            else
                                CallsiteInfo.argcheckresult.add("jointcheck-ctrlcnd"+"(" + j + ","+ i+ ")")
                            //println "\t[*] "+CallsiteInfo.argcheckresult
                            //return CallsiteInfo
                        }
                    }
                }
            }
        }
    }

    //5-c. 非控制依赖条件的参数检查
    //查看参数和非控制依赖条件语句之间是否有共同的定义语句,并且其条件语句代码体中有对参数变量的重定义
    //i. 查看条件语句的控制结构体中是否保护函数的定义语句. ii. 看条件语句中参与了多少个参数.
    //fei kongzhi yilai shuoming dui fuction de zhixing meiyou yingxiang. suoyi yaoqiu qi you gaibian arg de canshu dingyi.
    //println "\t\t3. 非控制依赖条件的参数检查 "
    for(cndnoctrl in CallsiteInfo.cndlistincfgpathNOcontrol){
        cndnoctrl_varandsymbol_list = []
        cndnoctrl_varandsymbol_list.addAll(getdefvar(cndnoctrl))
        cndnoctrl_varandsymbol_list.addAll(getsymbolset(cndnoctrl))
        //println "\t\t非控制条件的影响变量集: " + cnd_varandsymbol_list
        cndnoctrl_defstmtlist_intrap = getdefineStmtsofcfgnode(cndnoctrl)
        //println "\t\t非控制定义语句集: " + cndnoctrl_defstmtlist_intrap
        func_defstmt = getdefineStmtsofcfgnode(cfgnodeid)
        //println "\t\tcallsite的定义语句集: " + func_defstmt
        func_defstmt.retainAll(cndnoctrl_defstmtlist_intrap)
        argindexlist =[]
        if(func_defstmt.size()>0)
        {
            num = 0
            for (i=0;i<num_args;i++){
                tmplist=[]
                tmplist.addAll(cndnoctrl_varandsymbol_list)
                tmplist.retainAll(argset_varandsymbol_list[i])
                if(tmplist.size()>0){
                    //该条件语句的代码体中是否对参数变量进行了重定义?首先获取条件语句控制的语句节点集,然后查看其中是否有参数定义相关的节点.
                    //获取控制节点集的方法: 从条件语句出发,沿着控制依赖边CONTROLS可以获取所有与之条件直接相关的语句.
                    //注意其条件语句代码体内部的条件语句下一层的语句是无法直接获取,需要递归间接获取,但此处不需要.
                    //此处获取条件cndnotrl控制的语句节点列表,不需考虑语句节点为条件语句的情况,因为cndlistincfgpathNOcontrol已经获取了所有的
                    //CFG路径上的条件语句,故无需递归获取.
                    num = num + 1
                    argindexlist.add(i)
                }
            }
            Collections.sort(argindexlist)
            if(num >= 2){
                //CallsiteInfo.argcheckresult = "jointcheck-noctrlcnd"
                CallsiteInfo.argcheckresult.add("jointcheck-noctrlcnd"+"(" + argindexlist+ ")")
                //return CallsiteInfo
            }
            if(num == 1){
                //CallsiteInfo.argcheckresult = "singlcheck-noctrlcnd"
                CallsiteInfo.argcheckresult.add("singlcheck-noctrlcnd"+"(" + argindexlist + ")")
                //return CallsiteInfo
            }
        }
    }
    //println "\t\t"+CallsiteInfo.argcheckresult
    CallsiteInfo.argcheckresult.unique()
    return  CallsiteInfo;
}

//class Callee
//获取callee相关信息的入口
Object.metaClass.getCallOpsInfoList_intrap = {

    //println "*I. getCallOpsInfoList_intrap() begin"
    callinfolist = []
    calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList() //获取所有函数列表
    //calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList()[180]//memcpy

    num_call = calllist.size();
    println "calllist num:"+ num_call
    index_call = 0
    for (callname in calllist) //依次处理单个函数
    {
        //sqlite3.18.0项目中assert函数执行不结束，在此简单跳过处理。
        if(callname.code == 'assert')
            continue
        println index_call + " / " + num_call + " :: " + callname.code
        index_call = index_call + 1
        def callinfo = new CallInfo_intrap()
        callinfo.id = callname.id
        callinfo.code = callname.code
        callSiteIds=getCallsTo(callinfo.code).id.toList() //获取函数的调用实例ID列表
        //callSiteIds=getCallsTo(callinfo.code).id.toList()[520]//论文中的sink
        callinfo.callsiteNums = callSiteIds.size()
        for(callSite in callSiteIds){   //处理每个调用实例
            callinfo.callsiteinfolist.add(createCallsiteInfo_intrap(callSite))
        }
        callinfolist.add(callinfo)
    }
    calls = convCallOpsInfoList_intrap(callinfolist) //格式化输出
    //return callinfolist;
    return calls;

}

//获取列表的函数信息
Object.metaClass.getCallOpsInfoList_intrap_samples = {

    //println "*I. getCallOpsInfoList_intrap() begin"
    samples = [
            'abs',
            'atof',
            'atoi',
            'atol',
            'ceil',
            'closedir',
            'exit',
            'exp',
            'fstat',
            'getpid',
            'gettimeofday',
            'getuid',
            'isalnum',
            'isalpha',
            'isdigit',
            'islower',
            'isprint',
            'isspace',
            'isupper',
            'localtime',
            'mktime',
            'qsort',
            'readdir',
            'rewind',
            'sleep',
            'sqrt',
            'strtol',
            'strtoul',
            'system',
            'time',
            'tolower',
            'toupper',
            'memcpy',
            'free',
            'memmove',
            'memset',
            'strcat',
            'strcmp',
            'strcpy',
            'strlen',
            'strncat',
            'strncpy',
            'read',
            'write',
            'fclose',
            'fdopen',
            'fgets',
            'fileno',
            'fputc',
            'fputs',
            'fread',
            'fseek',
            'ftell',
            'fwrite',
            'gets',
            'fprintf',
            'fscanf',
            'printf',
            'scanf',
            'sprintf'
    ]

    callinfolist = []
    //calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList() //获取所有函数列表
    //calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList()[180]//memcpy

    num_call = samples.size();
    println "samples num:"+ num_call
    index_call = 0
    for (callname in samples) //依次处理单个函数
    {
        //sqlite3.18.0项目中assert函数执行不结束，在此简单跳过处理。
        if(callname == 'assert')
            continue
        println index_call + " / " + num_call + " :: " + callname
        index_call = index_call + 1
        def callinfo = new CallInfo_intrap()
        callinfo.id = 0
        callinfo.code = callname
        callSiteIds=getCallsTo(callinfo.code).id.toList() //获取函数的调用实例ID列表
        //callSiteIds=getCallsTo(callinfo.code).id.toList()[520]//论文中的sink
        callinfo.callsiteNums = callSiteIds.size()
        for(callSite in callSiteIds){   //处理每个调用实例
            callinfo.callsiteinfolist.add(createCallsiteInfo_intrap(callSite))
        }
        callinfolist.add(callinfo)
    }
    calls = convCallOpsInfoList_intrap(callinfolist) //格式化输出
    //return callinfolist;
    return calls;

}
// 将函数的实例信息进行格式化转换
Object.metaClass.convCallOpsInfoList_intrap = {callinfolist ->
    println "\n# 已分析call的数量" + callinfolist.size()
    def calls = callinfolist._().transform{
        [
                it.id,
                it.code,
                it.callsiteNums,
                it.callsiteinfolist._().transform{
                    [
                        it.callsiteid,
                        it.callsitecode,
                        it.argcheckresult,
                        it.cndlistbycontrol,
                        it.cndlistincfgpathNOcontrol,
                        it.argsinfolist._().transform{
                            [
                                    it.argid,
                                    it.argcode,
                                    it.symbolset,
                                    it.definestatments,
                                    it.defvar
                            ]
                        }
                    ]
                }
        ]
    }

    return calls
}
