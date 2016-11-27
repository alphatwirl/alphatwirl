# Tai Sakuma <tai.sakuma@cern.ch>
from .WeightCalculatorOne import WeightCalculatorOne

##__________________________________________________________________||
class Reader(object):
    def __init__(self, keyValComposer, summary, nextKeyComposer = None,
                 weightCalculator = WeightCalculatorOne()):
        self.keyValComposer = keyValComposer
        self.summary = summary
        self.weightCalculator = weightCalculator
        self.nextKeyComposer = nextKeyComposer

    def begin(self, event):
        self.keyValComposer.begin(event)

    def event(self, event):
        keyvals = self.keyValComposer(event)
        weight = self.weightCalculator(event)
        for key, val in keyvals:
            self.summary.add(key = key, val = val, weight = weight)

    def end(self):
        if self.nextKeyComposer is None: return
        for key in sorted(self.summary.keys()):
            nextKeys = self.nextKeyComposer(key)
            for nextKey in nextKeys: self.summary.add_key(nextKey)

    def copy_from(self, src):
        self.summary.copy_from(src.summary)

    def results(self):
        return self.summary

##__________________________________________________________________||
