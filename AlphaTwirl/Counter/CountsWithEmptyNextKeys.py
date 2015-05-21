# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
from CountsBase import CountsBase

##____________________________________________________________________________||
class CountsWithEmptyNextKeys(CountsBase):

    def __init__(self, countMethod):
        self._countMethod = countMethod

    def count(self, key, weight):
        nextKeys = self.nextKeyComposer(key)
        for nextKey in nextKeys: self._countMethod.addKey(nextKey)
        self._countMethod.count(key, weight)

    def valNames(self):
        return self._countMethod.valNames()

    def setResults(self, results):
        self._countMethod.setResults(results)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CountsWithEmptyNextKeysFactory(object):

    def __init__(self, countMethodClass):
        self._countMethodClass = countMethodClass

    def __call__(self):
        return CountsWithEmptyNextKeys(self._countMethodClass())

##____________________________________________________________________________||
