import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockCounts(object):
    def __init__(self):
        self._counts = [ ]

    def count(self, key, weight):
        self._counts.append((key, weight))

    def results(self):
        return self._counts

##____________________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class MockKeyComposer(object):
    def __init__(self, keys = [ ]):
        self.keys = keys

    def __call__(self, event):
        return self.keys.pop()

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
        keys = [(12, ), None, (14, ), (11, )]
        keycomposer = MockKeyComposer(keys)
        counter = Counter.Counter(('var', ), keycomposer, counts, MockWeightCalculator())
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

    def test_keynames(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        self.assertEqual(('var', ), counter.keynames())

##____________________________________________________________________________||
class TestCounterBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CounterBuilder(MockCounts, ('var_bin', ), MockKeyComposer())
        counter1 = builder()
        self.assertEqual(('var_bin', ), counter1._keynames)
        self.assertIsInstance(counter1._keyComposer, MockKeyComposer)
        self.assertIsInstance(counter1._countMethod, MockCounts)

    def test_counterMethods_differentInstances(self):
        builder = Counter.CounterBuilder(MockCounts, ('var_bin', ), MockKeyComposer())
        counter1 = builder()
        counter2 = builder()
        self.assertIsNot(counter1._countMethod, counter2._countMethod)

##____________________________________________________________________________||
