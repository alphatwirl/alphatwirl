# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
from CountsBase import CountsBase

##____________________________________________________________________________||
class CountsWithEmptyKeysInGap(CountsBase):

    def __init__(self, countMethod, keyGapKeeper):
        self._countMethod = countMethod
        self._keyGapKeeper = keyGapKeeper

    def count(self, key, weight):
        newkeys = self._keyGapKeeper.update(key)
        self._countMethod.addKeys(newkeys)
        self._countMethod.count(key, weight)

    def valNames(self):
        return self._countMethod.valNames()

    def setResults(self, results):
        self._countMethod.setResults(results)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapAndNext(CountsBase):

    def __init__(self, countMethod, keyGapKeeper):
        self._countMethod = countMethod
        self._keyGapKeeper = keyGapKeeper

    def count(self, key, weight):
        newkeys = self._keyGapKeeper.update(key)
        self._countMethod.addKeys(newkeys)
        nextKey = self._keyGapKeeper.next(key)
        newkeys = self._keyGapKeeper.update(nextKey)
        self._countMethod.addKeys(newkeys)
        self._countMethod.count(key, weight)

    def valNames(self):
        return self._countMethod.valNames()

    def setResults(self, results):
        self._countMethod.setResults(results)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapBuilder(object):

    def __init__(self, countMethodClass, keyGapKeeperClass):
        self._countMethodClass = countMethodClass
        self._keyGapKeeperClass = keyGapKeeperClass

    def __call__(self):
        return CountsWithEmptyKeysInGap(self._countMethodClass(), self._keyGapKeeperClass())

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapAndNextBuilder(object):

    def __init__(self, countMethodClass, keyGapKeeperClass):
        self._countMethodClass = countMethodClass
        self._keyGapKeeperClass = keyGapKeeperClass

    def __call__(self):
        return CountsWithEmptyKeysInGapAndNext(self._countMethodClass(), self._keyGapKeeperClass())

##____________________________________________________________________________||
