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

    def count(self, key, weight):
        newkeys = self._keyMaxKeeper.update(key)
        self._countMethod.addKeys(newkeys)
        nextKey = self._keyMaxKeeper.next(key)
        newkeys = self._keyMaxKeeper.update(nextKey)
        self._countMethod.addKeys(newkeys)
        self._countMethod.count(key, weight)

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CountsWithEmptyKeysInGapBuilder(object):

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
class KeyMinMaxKeeper(object):
    def __init__(self, binnings):
        self._binnings = binnings

        self._keys = None
        self._keyMin = None
        self._keyMax = None

    def update(self, key):
        if self._keys is None:
            self._keyMin = key
            self._keyMax = key
            self._keys = [key]
            return [ ]

        newMin = tuple([min(e) for e in zip(self._keyMin, key)])
        newMax = tuple([max(e) for e in zip(self._keyMax, key)])

        if newMin == self._keyMin and newMax == self._keyMax: return [ ]

        self._keyMin = newMin
        self._keyMax = newMax

        keys = self.createAllKeysBetween(newMin, newMax)
        ret = [k for k in keys if k not in self._keys]
        self._keys = keys

        return ret

    def createAllKeysBetween(self, key1, key2):
        newBins = [ ]
        for i in range(len(key2)):
            newBin = [ ]
            b = key1[i]
            while b <= key2[i]:
                newBin.append(b)
                b_ = self._binnings[i].next(b)
                if b == b_: break
                b = b_
            newBins.append(newBin)
        ret = list(itertools.product(*newBins))
        return ret

    def next(self, key):
        return tuple([binning.next(bin) for bin, binning in zip(key, self._binnings)])

##____________________________________________________________________________||
class KeyMinMaxKeeperBuilder(object):

    def __init__(self, binnings):
        self.binnings = binnings

    def __call__(self):
        return KeyMinMaxKeeper(self.binnings)

##____________________________________________________________________________||
