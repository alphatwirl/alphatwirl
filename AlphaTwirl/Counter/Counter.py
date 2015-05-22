# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

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
            if self.nextKeyComposer is not None:
                nextKeys = self.nextKeyComposer(key)
                for nextKey in nextKeys: self.countMethod.addKey(nextKey)
            self.countMethod.count(key, weight)

    def end(self):
        pass

    def valNames(self):
        return self.countMethod.valNames()

    def setResults(self, results):
        self.countMethod.setResults(results)

    def results(self):
        return self.countMethod.results()

##____________________________________________________________________________||
