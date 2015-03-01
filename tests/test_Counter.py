import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockBinning(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##____________________________________________________________________________||
class MockCounts(object):
    def __init__(self):
        self._counts = [ ]
        self._keys = [ ]

    def count(self, key, weight):
        self._counts.append((key, weight))

    def addKeys(self, keys):
        self._keys.extend(keys)

    def results(self):
        return self._counts

##____________________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class MockKeyComposer(object):
    def __init__(self):
        self._keys = [(13, ), (11, )]
        self._binning = MockBinning()

    def __call__(self, event):
        return self._keys.pop()

    def binnings(self):
        return (self._binning, )

##____________________________________________________________________________||
class TestMockKeyComposer(unittest.TestCase):

    def test_call(self):
        keycomposer = MockKeyComposer()
        self.assertEqual((11, ), keycomposer(MockEvent()))
        self.assertEqual((13, ), keycomposer(MockEvent()))

##____________________________________________________________________________||
class TestCounter(unittest.TestCase):

    def test_results(self):
        counts = MockCounts()
        counter = Counter.Counter(('var', ), MockKeyComposer(), counts, MockWeightCalculator())
        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

    def test_keynames(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        self.assertEqual(('var', ), counter.keynames())

    def test_addKeys(self):
        counts = MockCounts()
        counter = Counter.Counter(('var', ), MockKeyComposer(), counts, MockWeightCalculator(), addEmptyKeys = True)
        counter.event(MockEvent())
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([ ], counts._keys)

        counter.event(MockEvent())
        self.assertEqual([((11, ), 1.0), ((13, ), 1.0)], counts._counts)
        self.assertEqual([(12,), (13,)], counts._keys)

    def test_addKeys_disabled(self):
        counts = MockCounts()
        counter = Counter.Counter(('var', ), MockKeyComposer(), counts, MockWeightCalculator())
        counter.event(MockEvent())
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([ ], counts._keys)

        counter.event(MockEvent())
        self.assertEqual([((11, ), 1.0), ((13, ), 1.0)], counts._counts)
        self.assertEqual([ ], counts._keys)

##____________________________________________________________________________||
class TestCounterBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CounterBuilder(('var_bin', ), MockKeyComposer(), MockCounts)
        counter1 = builder()
        self.assertEqual(('var_bin', ), counter1._keynames)
        self.assertIsInstance(counter1._keyComposer, MockKeyComposer)
        self.assertIsInstance(counter1._countMethod, MockCounts)

    def test_counterMethods_differentInstances(self):
        builder = Counter.CounterBuilder(('var_bin', ), MockKeyComposer(), MockCounts)
        counter1 = builder()
        counter2 = builder()
        self.assertIsNot(counter1._countMethod, counter2._countMethod)

##____________________________________________________________________________||
