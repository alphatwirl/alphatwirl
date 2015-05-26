# Tai Sakuma <tai.sakuma@cern.ch>
from NextKeyComposer import NextKeyComposer
from Counter import Counter

##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class CounterFactory(Counter):
    def __init__(self, countMethodClass, keyComposerFactory, binnings, weightCalculator = WeightCalculatorOne()):
        self._keyComposerFactory = keyComposerFactory
        self._countMethodClass = countMethodClass
        self._binnings = binnings
        self._weightCalculator = weightCalculator

    def __call__(self):

        return Counter(
            self._keyComposerFactory(),
            self._countMethodClass(),
            NextKeyComposer(self._binnings),
            self._weightCalculator
        )

##____________________________________________________________________________||