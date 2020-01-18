//by cl
//获取call各callsite的外部处理语句和实参的相关数据,其中参数之前的定义关系只考虑了一层,即直接相关,他们之间是可以通过symbol的递进传播可以有多层的间接联系.
//2016-06-02 09:27:46

//根据一个CFG节点获取它的前置条件id列表
def conditionslist_D=[]
Object.metaClass.getConditionsFromCfgNodeid_D = { cfgnodeid ->
    /**多个直接控制条件语句
    def controlslist = g.v(cfgnodeid).inE.has('label','CONTROLS').outV.id.toList()
    for(controlid in controlslist){
        if(controlid.code == "ENTRY"){
            break;
        }
        else {
            CallsiteInfo.conditionslist.add(controlid)
            controlslist.add(g.v(controlid).inE.has('label','CONTROLS').outV.id.toList())
        }
    }
    **/

    //假定每个CFG节点的直接控制条件语句只会有一个
    def controlids = g.v(cfgnodeid).inE.has('label','CONTROLS').outV.id.toList()
    for(controlid in controlids){
        if(g.v(controlid).code != "ENTRY"){
            if(conditionslist_D.contains(controlid))
                continue;
            conditionslist_D.add(controlid)
            getConditionsFromCfgNodeid_D(controlid)
        }
    }
    return conditionslist_D;
}

//判断一个id是否为CFGNode,并且是一个函数
Object.metaClass.IsCFGNodeACall = { cfgnodeid ->
    if(g.v(cfgnodeid).isCFGNode == "True")
    {
        if(g.v(cfgnodeid).outE('IS_AST_PARENT').inV.has('type','CallExpression').toList().code.contains(g.v(cfgnodeid).code))
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
    2. callsite调用的前置条件和其实参参与的条件语句不是包含与被包含的关系,是否需要整理?
**/
Object.metaClass.createCallsiteInfo_D = { callsiteid ->

    //println "createCallsiteInfo_D begin:" + callsiteid

    def CallsiteInfo = new CallsiteInfo();
    CallsiteInfo.callsiteid = callsiteid;
    CallsiteInfo.callsitecode = g.v(callsiteid).code;
    argSet = g.v(callsiteid)._().callToArguments().id.toList() //.sort()

    //获取条件语句的id列表HUnlock
    //此处有且一项,ExpressionStatement
    def cfgnodeid = g.v(callsiteid)._().statements().id.toList().toList()[0]
    conditionslist_D=[]
    if(cfgnodeid == null){
        CallsiteInfo.conditionslist = []
        CallsiteInfo.argsinfolist = []
        return CallsiteInfo;
    }
    else{
        //注意此处getConditionsFromCfgNodeid_D返回的也是list,所以要用addAll,而不是add
        CallsiteInfo.conditionslist.addAll(getConditionsFromCfgNodeid_D(cfgnodeid))
    }
    //println "get conditions over"
    //获取实参预操作信息
    def callsitelocation=g.v(cfgnodeid).location
    for(argid in argSet){
        def argGraph = new ArgInfo_D()
        argGraph.argid = argid
        argGraph.argcode = g.v(argid).code
        def symbolids = getSymbolNodeIds(g.v(argid))
        for(symbol_id in symbolids){
            def symbol2stmtids = g.v(symbol_id).in.has('isCFGNode','True').id.dedup().toList()
            for(symbolstmtlID in symbol2stmtids){
                //位于调用前的相关语句才有意义
                if(g.v(symbolstmtlID).location < callsitelocation){
                    if(g.v(symbolstmtlID).type!='Condition'){
                        if(IsDefined(symbol_id,symbolstmtlID)){
                            argGraph.stmtsleftlist.add(symbolstmtlID)
                            }
                        else{
                            argGraph.stmtsrightlist.add(symbolstmtlID)
                            }
                        if(IsCFGNodeACall(symbolstmtlID)){
                            argGraph.stmtiscalllist.add(symbolstmtlID)
                        }

                    }
                    else{
                        argGraph.conditionslist.add(symbolstmtlID)
                    }
                }
            }
        }
        CallsiteInfo.argsinfolist.add(argGraph)
    }
    return  CallsiteInfo;
}

Object.metaClass.createFuncOpsGraph_D = { functionid ->
    def funcGraph = new FuncOpsGraph()
    funcGraph.funcid = functionid;
    def paramidlist = g.v(functionid).out.has('type','FunctionDef').out.has('type','ParameterList').out.id.toList();
    for(paramid in paramidlist){
        def paramgraph = new ArgInfo_D()
        paramgraph.argid = paramid
        paramgraph.argcode = g.v(paramid).code

        def cfgnodeidlist = g.v(paramid).outE('REACHES').inV.id
        for(cfgnodeid in cfgnodeidlist){
            if(g.v(cfgnodeid).type == 'Condition'){
                paramgraph.conditionslist.add(cfgnodeid)
            }
            else{
                paramgraph.statementslist.add(cfgnodeid)
            }
        }

        funcGraph.paramsinfo.add(paramGraph)
    }
    /*
    def callsiteIds = getCallsTo(calleecode).id.toList()
    for(callsiteid in callsiteIds){
        def callsitegraph = new CallsiteInfo()
        callsitegraph = createCallsiteInfo_D(callsiteid)
        funcGraph.CallsiteInfolist.add(callsitegraph)
    }
    */
    //funcGraph.numoflines =
    return funcGraph;
}

//class Callee
Object.metaClass.getCallOpsInfoList_D = {

    println "**************getCallOpsInfoList_D begin**************"
    callinfolist = []
    calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList()
    //calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList()[180]//memcpy

    num_call = calllist.size();
    println "calllist num:"+ num_call
    i = 0
    for (callname in calllist)
    {
        println i + " / " + num_call + " :: " + callname.code
        i = i+1
        def callinfo = new CallInfo()
        callinfo.id = callname.id
        callinfo.code = callname.code
        callSiteIds=getCallsTo(callinfo.code).id.toList()
        //callSiteIds=getCallsTo(callinfo.code).id.toList()[520]//论文中的sink
        for(callSite in callSiteIds){
            callinfo.callsiteinfolist.add(createCallsiteInfo_D(callSite))
        }
        callinfo.callsiteNums = getCallsTo(callinfo.code).toList().size()
        callinfolist.add(callinfo)
    }
    println "**************getCallOpsInfoList_D end  **************"
    calls = convCallOpsInfoList_D(callinfolist)
    println "**************convCallOpsInfoList_D end  **************"
    //return callinfolist;
    return calls;

}


Object.metaClass.convCallOpsInfoList_D = {callinfolist ->
    println callinfolist.size()
    def calls = callinfolist._().transform{
        [
                it.id,
                it.code,
                it.callsiteNums,
                it.callsiteinfolist._().transform{
                [
                    it.callsiteid,
                    it.callsitecode,
                    it.conditionslist,
                    it.argsinfolist._().transform{
                        [
                                it.argid,
                                it.argcode,
                                it.conditionslist,
                                it.stmtsleftlist,
                                it.stmtsrightlist,
                                it.stmtiscalllist
                        ]
                    }
                ]}
        ]
    }
    return calls
}
