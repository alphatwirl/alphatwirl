# Tai Sakuma <sakuma@fnal.gov>
import itertools

##____________________________________________________________________________||
class CountsWithEmptyKeysInGap(object):

    def __init__(self, countMethod, keyMaxKeeper):
        self._countMethod = countMethod
        self._keyMaxKeeper = keyMaxKeeper

    def count(self, key, weight):
        newkeys = self._keyMaxKeeper.update(key)
        self._countMethod.addKeys(newkeys)
        self._countMethod.count(key, weight)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapAndNext(object):

    def __init__(self, countMethod, keyMaxKeeper):
        self._countMethod = countMethod
        self._keyMaxKeeper = keyMaxKeeper

        self._first = True

    def count(self, key, weight):
        if self._first:
            self._first = False
            self._keyMaxKeeper.update(key)
        nextKey = self._keyMaxKeeper.next(key)
        newkeys = self._keyMaxKeeper.update(nextKey)
        self._countMethod.addKeys(newkeys)
        self._countMethod.count(key, weight)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapBulder(object):

    def __init__(self, countMethodClass, keyMaxKeeperClass):
        self._countMethodClass = countMethodClass
        self._keyMaxKeeperClass = keyMaxKeeperClass

    def __call__(self):
        return CountsWithEmptyKeysInGap(self._countMethodClass(), self._keyMaxKeeperClass())

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapAndNextBuilder(object):

    def __init__(self, countMethodClass, keyMaxKeeperClass):
        self._countMethodClass = countMethodClass
        self._keyMaxKeeperClass = keyMaxKeeperClass

    def __call__(self):
        return CountsWithEmptyKeysInGapAndNext(self._countMethodClass(), self._keyMaxKeeperClass())

##____________________________________________________________________________||
class KeyMaxKeeper(object):
    def __init__(self, binnings):
        self._keyMax = None
        self._binnings = binnings

    def update(self, key):
        if self._keyMax is None:
            self._keyMax = key
            return [ ]
        newMax = tuple([max(e) for e in zip(self._keyMax, key)])
        ret = self.createAllKeysBetween(self._keyMax, newMax)
        self._keyMax = newMax
        return ret

    def createAllKeysBetween(self, oldMax, newMax):
        newBins = [ ]
        for i in range(len(newMax)):
            newBin = [ ]
            b = oldMax[i]
            while b <= newMax[i]:
                newBin.append(b)
                b = self._binnings[i].next(b)
            newBins.append(newBin)

        ret = list(itertools.product(*newBins))
        ret.remove(self._keyMax)
        return ret

    def next(self, key):
        return tuple([binning.next(bin) for bin, binning in zip(key, self._binnings)])

##____________________________________________________________________________||
class KeyMaxKeeperBuilder(object):

    def __init__(self, binnings):
        self.binnings = binnings

    def __call__(self):
        return KeyMaxKeeper(self.binnings)

##____________________________________________________________________________||
