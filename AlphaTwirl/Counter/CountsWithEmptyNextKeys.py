# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
from CountsBase import CountsBase

##____________________________________________________________________________||
class CountsWithEmptyNextKeys(CountsBase):

    def __init__(self, countMethod):
        self._countMethod = countMethod

    def count(self, key, weight):
        nextKeys = self.keyComposer.next(key)
        self._countMethod.addKeys(nextKeys)
        self._countMethod.count(key, weight)

    def valNames(self):
        return self._countMethod.valNames()

    def setResults(self, results):
        self._countMethod.setResults(results)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CountsWithEmptyNextKeysBuilder(object):

    def __init__(self, countMethodClass):
        self._countMethodClass = countMethodClass

    def __call__(self):
        return CountsWithEmptyNextKeys(self._countMethodClass())

##____________________________________________________________________________||
