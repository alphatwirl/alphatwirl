# Tai Sakuma <sakuma@fnal.gov>
import itertools

##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class Counter(object):
    def __init__(self, keyNames, keyComposer, countMethod, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposer = keyComposer
        self._countMethod = countMethod
        self._weightCalculator = weightCalculator

    def event(self, event):
        key = self._keyComposer(event)

        weight = self._weightCalculator(event)
        self._countMethod.count(key, weight)

    def keynames(self):
        return self._keynames

    def results(self):
        return self._countMethod.results()

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
class CountsWithEmptyKeysInGapBulder(object):

    def __init__(self, countMethodClass, keyMaxKeeperClass):
        self._countMethodClass = countMethodClass
        self._keyMaxKeeperClass = keyMaxKeeperClass

    def __call__(self):
        return CountsWithEmptyKeysInGap(self._countMethodClass(), self._keyMaxKeeperClass())

##____________________________________________________________________________||
class CounterBuilder(Counter):
    def __init__(self, countMethodClass, keyNames, keyComposer, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposer = keyComposer
        self._countMethodClass = countMethodClass
        self._weightCalculator = weightCalculator

    def __call__(self):
        return Counter(self._keynames, self._keyComposer, self._countMethodClass(), self._weightCalculator)

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

##____________________________________________________________________________||
