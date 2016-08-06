# Tai Sakuma <tai.sakuma@cern.ch>
from .WeightCalculatorOne import WeightCalculatorOne

##__________________________________________________________________||
class Counter(object):
    def __init__(self, keyValComposer, countMethod, nextKeyComposer = None,
                 weightCalculator = WeightCalculatorOne()):
        self.keyValComposer = keyValComposer
        self.countMethod = countMethod
        self.weightCalculator = weightCalculator
        self.nextKeyComposer = nextKeyComposer

    def begin(self, event):
        self.keyValComposer.begin(event)

    def event(self, event):
        keyvals = self.keyValComposer(event)
        weight = self.weightCalculator(event)
        for key, val in keyvals:
            self.countMethod.count(key, weight)

    def end(self):
        if self.nextKeyComposer is None: return
        for key in sorted(self.countMethod.keys()):
            nextKeys = self.nextKeyComposer(key)
            for nextKey in nextKeys: self.countMethod.addKey(nextKey)

    def valNames(self):
        return self.countMethod.valNames()

    def copyFrom(self, src):
        self.countMethod.copyFrom(src.countMethod)

    def results(self):
        return self.countMethod.results()

##__________________________________________________________________||
