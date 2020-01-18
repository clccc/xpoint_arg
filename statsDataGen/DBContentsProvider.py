#---------------------------
#code by Chenlin 2016-03-26
#uses pickle to save struct data to a file or load stract data from a file
#---------------------------
#coding:utf-8
from joern.all import JoernSteps


class DBContentsProvider:

    def __init__(self):
        self._initDatabaseConnection()

    def _initDatabaseConnection(self):

        self.j = JoernSteps()
        self.j.connectToDatabase()
        self.j.addStepsDir('steps/')

    def RunGremlinQuery(self, query):
        results = self.j.runGremlinQuery(query)
        return results

    def GetCalleesInfo(self):
        query = "getCalleeListInfo()"
        return self.j.runGremlinQuery(query)

    """
    Generate contents for a given selector, overwriting
    the contents currently held in cndToQueries memory by the server.
    """
    def generate(self, selector):
        query = """generateTaintLearnStructures(%s.id.toList())
        _()""" % (selector)
        for unused in self.j.runGremlinQuery(query): pass



if __name__ == '__main__':
    gen = DBContentsProvider()
    # gen.generate('g.v(12798)._()')
    gen.generate('getCallsTo("TIFFFetchData")._()')
    for x in gen.getSourceAPISymbols():
        print x
