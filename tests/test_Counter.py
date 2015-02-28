import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockBinning(object):
    def __call__(self, val):
        return val

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
    def __init__(self):
        self._keys = [(13, ), (11, )]
        pass

    def __call__(self, event):
        return self._keys.pop()

##____________________________________________________________________________||
class TestMockKeyComposer(unittest.TestCase):

    def test_call(self):
        keycomposer = MockKeyComposer()
        self.assertEqual((11, ), keycomposer(MockEvent()))
        self.assertEqual((13, ), keycomposer(MockEvent()))

##____________________________________________________________________________||
class TestCounter(unittest.TestCase):

    def test_results(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counter.results())

    def test_keynames(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        self.assertEqual(('var', ), counter.keynames())

##____________________________________________________________________________||
class TestCounterBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CounterBuilder(('var_bin', ), MockKeyComposer(), MockCounts)
        counter1 = builder()
        self.assertEqual(('var_bin', ), counter1._keynames)
        self.assertIsInstance(counter1._keyComposer, MockKeyComposer)
        self.assertIsInstance(counter1._countMethod, MockCounts)

        counter2 = builder()
        self.assertEqual(('var_bin', ), counter2._keynames)
        self.assertIsInstance(counter2._keyComposer, MockKeyComposer)
        self.assertIsInstance(counter2._countMethod, MockCounts)

        self.assertIs(counter1._keyComposer, counter2._keyComposer)
        self.assertIsNot(counter1._countMethod, counter2._countMethod)

##____________________________________________________________________________||
class TestKeyComposer_SingleVariable(unittest.TestCase):

    def test_call(self):
        keyComposer = Counter.KeyComposer_SingleVariable('var1', MockBinning())

        event = MockEvent()
        event.var1 = 12
        self.assertEqual((12, ), keyComposer(event))

##____________________________________________________________________________||
class TestKeyComposer_TwoVariables(unittest.TestCase):

    def test_call(self):
        keyComposer = Counter.KeyComposer_TwoVariables('var1', MockBinning(), 'var2', MockBinning())

        event = MockEvent()
        event.var1 = 15
        event.var2 = 22
        self.assertEqual((15, 22), keyComposer(event))

##____________________________________________________________________________||
