# Tai Sakuma <sakuma@fnal.gov>
import AlphaTwirl
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

        self._keyMaxKeeper = KeyMaxKeeper()

    def event(self, event):
        key = self._keyComposer(event)

        newkeys = self._keyMaxKeeper.update(key)
        self._countMethod.addKeys(newkeys)

        weight = self._weightCalculator(event)
        self._countMethod.count(key, weight)

    def keynames(self):
        return self._keynames

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CounterBuilder(Counter):
    def __init__(self, keyNames, keyComposer, countMethodClass, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposer = keyComposer
        self._countMethodClass = countMethodClass
        self._weightCalculator = weightCalculator

    def __call__(self):
        return Counter(self._keynames, self._keyComposer, self._countMethodClass(), self._weightCalculator)

##____________________________________________________________________________||
class KeyMaxKeeper(object):
    def __init__(self):
        self._keyMax = None

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
                b = b + 1
            newBins.append(newBin)

        ret = list(itertools.product(*newBins))
        ret.remove(self._keyMax)
        return ret

##____________________________________________________________________________||
class KeyComposer_SingleVariable(object):
    def __init__(self, varName, binning):
        self._varName = varName
        self._binning = binning

    def __call__(self, event):
        var = getattr(event, self._varName)
        var_bin = self._binning(var)
        return (var_bin, )

    def binnings(self):
        return (self._binning, )

##____________________________________________________________________________||
class KeyComposer_TwoVariables(object):
    def __init__(self, varName1, binning1, varName2, binning2):
        self._varName1 = varName1
        self._binning1 = binning1
        self._varName2 = varName2
        self._binning2 = binning2

    def __call__(self, event):
        var1 = getattr(event, self._varName1)
        var1_bin = self._binning1(var1)
        var2 = getattr(event, self._varName2)
        var2_bin = self._binning2(var2)
        return (var1_bin, var2_bin)

    def binnings(self):
        return (self._binning1, self._binning2)

##____________________________________________________________________________||
