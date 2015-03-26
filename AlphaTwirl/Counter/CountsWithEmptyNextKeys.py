# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
from CountsBase import CountsBase

##____________________________________________________________________________||
class CountsWithEmptyNextKeys(CountsBase):

    def __init__(self, countMethod, keyGapKeeper):
        self._countMethod = countMethod
        self._keyGapKeeper = keyGapKeeper

    def count(self, key, weight):
        nextKeys = self._keyGapKeeper.next(key)
        self._countMethod.addKeys(nextKeys)
        self._countMethod.count(key, weight)

    def setResults(self, results):
        self._countMethod.setResults(results)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
