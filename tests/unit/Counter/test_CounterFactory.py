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
class TestCounterFactory(unittest.TestCase):

    def test_call(self):
        builder = Counter.CounterFactory(MockCounts, MockKeyComposer, MockBinning())
        counter1 = builder()
        self.assertIsInstance(counter1._keyComposer, MockKeyComposer)
        self.assertIsInstance(counter1._countMethod, MockCounts)

    def test_counterMethods_differentInstances(self):
        builder = Counter.CounterFactory(MockCounts, MockKeyComposer, MockBinning())
        counter1 = builder()
        counter2 = builder()
        self.assertIsNot(counter1._countMethod, counter2._countMethod)

##____________________________________________________________________________||
