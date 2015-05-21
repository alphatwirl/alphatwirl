import AlphaTwirl.Counter as Counter
import unittest
import pickle

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockCounts(Counter.CountsBase):
    def __init__(self):
        self._counts = [ ]

    def count(self, key, weight):
        self._counts.append((key, weight))

    def valNames(self):
        return ('n', 'nvar')

    def setResults(self, results):
        self._counts = results

    def results(self):
        return self._counts

##____________________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class MockBinning(object): pass

##____________________________________________________________________________||
class MockKeyComposer(object):
    def __init__(self, listOfKeys = [ ]):
        self.listOfKeys = listOfKeys
        self._begin = None

    def begin(self, event):
        self._begin = event

    def __call__(self, event):
        return self.listOfKeys.pop()

##____________________________________________________________________________||
class TestMockKeyComposer(unittest.TestCase):

    def test_call(self):
        keys = [(13, 5), (11, 2), (11, 10), (2, 22)]
        keycomposer = MockKeyComposer(keys)
        self.assertEqual((2, 22), keycomposer(MockEvent()))
        self.assertEqual((11, 10), keycomposer(MockEvent()))
        self.assertEqual((11, 2), keycomposer(MockEvent()))
        self.assertEqual((13, 5), keycomposer(MockEvent()))
        self.assertRaises(IndexError, keycomposer, MockEvent())

##____________________________________________________________________________||
class TestCounter(unittest.TestCase):

    def test_events(self):
        counts = MockCounts()
        listOfKeys = [[(11, ), (12, )], [(12, )], [ ], [(14, )], [(11, )]]
        keycomposer = MockKeyComposer(listOfKeys)
        counter = Counter.Counter(('var', ), keycomposer, counts, MockWeightCalculator())

        event = MockEvent()
        counter.begin(event)
        self.assertEqual(event, keycomposer._begin)

        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0)], counts.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0), ((11,), 1.0), ((12,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0), ((11,), 1.0), ((12,), 1.0)], counts.results())

        counter.end()

    def test_keynames(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        self.assertEqual(('var', ), counter.keynames())

    def test_setResults(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        self.assertEqual([ ], counter.results())
        counter.setResults([((11, ), 1.0)])
        self.assertEqual([((11,), 1.0)], counter.results())

##____________________________________________________________________________||
class TestCounterBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CounterBuilder(MockCounts, ('var_bin', ), MockKeyComposer, MockBinning())
        counter1 = builder()
        self.assertEqual(('var_bin', ), counter1._keynames)
        self.assertIsInstance(counter1._keyComposer, MockKeyComposer)
        self.assertIsInstance(counter1._countMethod, MockCounts)

    def test_counterMethods_differentInstances(self):
        builder = Counter.CounterBuilder(MockCounts, ('var_bin', ), MockKeyComposer, MockBinning())
        counter1 = builder()
        counter2 = builder()
        self.assertIsNot(counter1._countMethod, counter2._countMethod)

##____________________________________________________________________________||
