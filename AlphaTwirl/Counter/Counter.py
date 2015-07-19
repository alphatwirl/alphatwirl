# Tai Sakuma <tai.sakuma@cern.ch>
from .WeightCalculatorOne import WeightCalculatorOne

##____________________________________________________________________________||
class Counter(object):
    def __init__(self, keyComposer, countMethod, nextKeyComposer = None,
                 weightCalculator = WeightCalculatorOne()):
        self.keyComposer = keyComposer
        self.countMethod = countMethod
        self.weightCalculator = weightCalculator
        self.nextKeyComposer = nextKeyComposer

    def begin(self, event):
        self.keyComposer.begin(event)

    def event(self, event):
        keys = self.keyComposer(event)
        weight = self.weightCalculator(event)
        for key in keys:
            self.countMethod.count(key, weight)

    def end(self):
        if self.nextKeyComposer is None: return
        for key in sorted(self.countMethod.keys()):
            nextKeys = self.nextKeyComposer(key)
            for nextKey in nextKeys: self.countMethod.addKey(nextKey)

    def valNames(self):
        return self.countMethod.valNames()

    def setResults(self, results):
        self.countMethod.setResults(results)

    def results(self):
        return self.countMethod.results()

##____________________________________________________________________________||
