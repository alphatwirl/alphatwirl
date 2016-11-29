# Tai Sakuma <tai.sakuma@cern.ch>
from .WeightCalculatorOne import WeightCalculatorOne

##__________________________________________________________________||
class Reader(object):
    def __init__(self, keyValComposer, summarizer, nextKeyComposer = None,
                 weightCalculator = WeightCalculatorOne()):
        self.keyValComposer = keyValComposer
        self.summarizer = summarizer
        self.weightCalculator = weightCalculator
        self.nextKeyComposer = nextKeyComposer

    def __repr__(self):
        return '{}(keyValComposer = {!r}, summarizer = {!r}, weightCalculator = {!r}, nextKeyComposer = {!r})'.format(
            self.__class__.__name__,
            self.keyValComposer,
            self.summarizer,
            self.weightCalculator,
            self.nextKeyComposer
        )

    def begin(self, event):
        self.keyValComposer.begin(event)

    def event(self, event):
        keyvals = self.keyValComposer(event)
        weight = self.weightCalculator(event)
        for key, val in keyvals:
            self.summarizer.add(key = key, val = val, weight = weight)

    def end(self):
        if self.nextKeyComposer is None: return
        for key in sorted(self.summarizer.keys()):
            nextKeys = self.nextKeyComposer(key)
            for nextKey in nextKeys: self.summarizer.add_key(nextKey)

    def copy_from(self, src):
        self.summarizer.copy_from(src.summarizer)

    def results(self):
        return self.summarizer

##__________________________________________________________________||
