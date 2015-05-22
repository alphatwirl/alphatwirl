# Tai Sakuma <tai.sakuma@cern.ch>
from CountsWithEmptyNextKeys import CountsWithEmptyNextKeys
from NextKeyComposer import NextKeyComposer
from Counter import Counter


##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class CounterFactory(Counter):
    def __init__(self, countMethodClass, keyNames, keyComposerFactory, binnings, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposerFactory = keyComposerFactory
        self._countMethodClass = countMethodClass
        self._binnings = binnings
        self._weightCalculator = weightCalculator

    def __call__(self):
        countMethod = self._countMethodClass()
        if isinstance(countMethod, CountsWithEmptyNextKeys):
            nextKeyComposer = NextKeyComposer(self._binnings)
            countMethod.nextKeyComposer = nextKeyComposer

        return Counter(
            self._keynames,
            self._keyComposerFactory(),
            countMethod,
            self._weightCalculator
        )

##____________________________________________________________________________||
