# Tai Sakuma <sakuma@fnal.gov>
import AlphaTwirl

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
class CounterBuilder(Counter):
    def __init__(self, keyNames, keyComposer, countMethodClass, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposer = keyComposer
        self._countMethodClass = countMethodClass
        self._weightCalculator = weightCalculator

    def __call__(self):
        return Counter(self._keynames, self._keyComposer, self._countMethodClass(), self._weightCalculator)

##____________________________________________________________________________||
class KeyComposer_SingleVariable(object):
    def __init__(self, varName, binning):
        self._varName = varName
        self._binning = binning

    def __call__(self, event):
        var = getattr(event, self._varName)
        var_bin = self._binning(var)
        return (var_bin, )

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

##____________________________________________________________________________||
