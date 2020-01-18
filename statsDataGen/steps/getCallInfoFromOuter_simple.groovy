//by cl
//2016-06-02 09:27:46

//根据一个CFG节点获取它的前置条件id列表
def conditionslist=[]
Object.metaClass.getConditionsFromCfgNodeid = { cfgnodeid ->
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
            if(conditionslist.contains(controlid))
                continue;
            conditionslist.add(controlid)
            getConditionsFromCfgNodeid(controlid)
        }
    }
    return conditionslist;
}

/**
 Create a CallsiteInfo:
 问题:1. //此处有且一项,ExpressionStatement
    def cfgnodeid = g.v(callsiteid)._().statements().id.toList().toList()[0]
    中获取为null的后面的语句和条件列表直接置为空,但实际存在出入.
    2. callsite调用的前置条件和其实参参与的条件语句不是包含与被包含的关系,是否需要整理?
**/
Object.metaClass.createCallsiteInfo = { callsiteid ->

    println "createCallsiteInfo begin:" + callsiteid

    def CallsiteInfo = new CallsiteInfo();
    CallsiteInfo.callsiteid = callsiteid;
    CallsiteInfo.callsitecode = g.v(callsiteid).code;
    argSet = g.v(callsiteid)._().callToArguments().id.toList() //.sort()

    println "createCallsiteInfo: callsiteid= " + callsiteid
    //获取条件语句的id列表HUnlock
    //此处有且一项,ExpressionStatement
    def cfgnodeid = g.v(callsiteid)._().statements().id.toList().toList()[0]
    conditionslist=[]
    if(cfgnodeid == null){
        CallsiteInfo.conditionslist = []
        CallsiteInfo.argsinfolist = []
        return CallsiteInfo;
    }
    else{
        //注意此处getConditionsFromCfgNodeid返回的也是list,所以要用addAll,而不是add
        CallsiteInfo.conditionslist.addAll(getConditionsFromCfgNodeid(cfgnodeid))
    }
    println "get conditions over"
    //获取实参预操作信息
    def location=g.v(cfgnodeid).location
    for(argid in argSet){
        def argGraph = new ArgInfo_S()
        argGraph.argid = argid
        argGraph.argcode = g.v(argid).code
        def symbolnodeids = getSymbolNodeIds(g.v(argid))
        for(symbolnode in symbolnodeids){
            def symbolstmts = g.v(symbolnode).in.has('isCFGNode','True').id.dedup().toList()
            for(sysmbolstatementid in symbolstmts){
                //位于调用前的相关语句才有意义
                if(g.v(sysmbolstatementid).location < location){
                    if(g.v(sysmbolstatementid).type!='Condition'){
                        argGraph.statementslist.add(sysmbolstatementid)
                    }
                    else{
                        argGraph.conditionslist.add(sysmbolstatementid)
                    }
                }
            }
        }
        CallsiteInfo.argsinfolist.add(argGraph)
    }
    return  CallsiteInfo;
}

Object.metaClass.createFuncOpsGraph = { functionid ->
    def funcGraph = new FuncOpsGraph()
    funcGraph.funcid = functionid;
    def paramidlist = g.v(functionid).out.has('type','FunctionDef').out.has('type','ParameterList').out.id.toList();
    for(paramid in paramidlist){
        def paramgraph = new ArgInfo_S()
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
        callsitegraph = createCallsiteInfo(callsiteid)
        funcGraph.CallsiteInfolist.add(callsitegraph)
    }
    */
    //funcGraph.numoflines =
    return funcGraph;
}

//class Callee
Object.metaClass.getCallOpsInfoList = {

    println "**************getCallOpsInfoList begin**************"

    callinfolist = []
    calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList()
    //calllist = g.V.has('type','Callee').as('x').code.dedup().back('x').toList()[180]//memcpy
    for (callname in calllist)
    {
        println "calls name:" + callname.code
        def callinfo = new CallInfo()
        callinfo.id = callname.id
        callinfo.code = callname.code
        callSiteIds=getCallsTo(callinfo.code).id.toList()
        //callSiteIds=getCallsTo(callinfo.code).id.toList()[520]//论文中的sink
        for(callSite in callSiteIds){
            callinfo.callsiteinfolist.add(createCallsiteInfo(callSite))
        }
        callinfo.callsiteNums = getCallsTo(callinfo.code).toList().size()
        callinfolist.add(callinfo)
    }
    println "**************getCallOpsInfoList end  **************"
    calls = convCallOpsInfoList(callinfolist)
    return calls;

}


Object.metaClass.convCallOpsInfoList = {callinfolist ->
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
                                it.statementslist,
                                it.conditionslist
                        ]
                    }
                ]}
        ]
    }
    return calls
}
