# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
from CountsBase import CountsBase
from KeyGapKeeper import KeyGapKeeper

##____________________________________________________________________________||
class CountsWithEmptyKeysInGap(CountsBase):

    def __init__(self, countMethod):
        self._countMethod = countMethod

    def setKeyComposer(self, keyComposer):
        super(CountsWithEmptyKeysInGap, self).setKeyComposer(keyComposer)
        self._keyGapKeeper = KeyGapKeeper(self.keyComposer.binnings())

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

    def __init__(self, countMethod):
        self._countMethod = countMethod

    def setKeyComposer(self, keyComposer):
        super(CountsWithEmptyKeysInGapAndNext, self).setKeyComposer(keyComposer)
        self._keyGapKeeper = KeyGapKeeper(self.keyComposer.binnings())

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

    def __init__(self, countMethodClass):
        self._countMethodClass = countMethodClass

    def __call__(self):
        return CountsWithEmptyKeysInGap(self._countMethodClass())

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapAndNextBuilder(object):

    def __init__(self, countMethodClass):
        self._countMethodClass = countMethodClass

    def __call__(self):
        return CountsWithEmptyKeysInGapAndNext(self._countMethodClass())

##____________________________________________________________________________||
