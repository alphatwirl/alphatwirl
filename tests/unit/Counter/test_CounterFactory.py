import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockCounts(object): pass

##____________________________________________________________________________||
class MockBinning(object): pass

##____________________________________________________________________________||
class MockKeyComposer(object): pass

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

    def test_keyComposer_differentInstances(self):
        builder = Counter.CounterFactory(MockCounts, MockKeyComposer, MockBinning())
        counter1 = builder()
        counter2 = builder()
        self.assertIsNot(counter1._keyComposer, counter2._keyComposer)

##____________________________________________________________________________||
