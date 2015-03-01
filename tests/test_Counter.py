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
class TestKeyMaxKeeper(unittest.TestCase):

    def setUp(self):
        self.keeper = Counter.KeyMaxKeeper()
        self.keeper.update((11, 8))

    def test_None_at_beginning(self):
        keyMax = Counter.KeyMaxKeeper()
        self.assertIsNone(keyMax._keyMax)

    def test_two_elements_lower_lower(self):
        key = (10, 6)
        expected = [ ]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((11, 8), self.keeper._keyMax)

    def test_two_elements_lower_same(self):
        key = (10, 8)
        expected = [ ]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((11, 8), self.keeper._keyMax)

    def test_two_elements_lower_higher(self):
        key = (10, 13)
        expected = [(11, 9), (11, 10), (11, 11), (11, 12), (11, 13)]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((11, 13), self.keeper._keyMax)

    def test_two_elements_same_lower(self):
        key = (11, 6)
        expected = [ ]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((11, 8), self.keeper._keyMax)

    def test_two_elements_same_same(self):
        key = (11, 8)
        expected = [ ]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((11, 8), self.keeper._keyMax)

    def test_two_elements_same_higher(self):
        key = (11, 13)
        expected = [(11, 9), (11, 10), (11, 11), (11, 12), (11, 13)]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((11, 13), self.keeper._keyMax)

    def test_two_elements_higher_lower(self):
        key = (15, 6)
        expected = [(12, 8), (13, 8), (14, 8), (15, 8)]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((15, 8), self.keeper._keyMax)

    def test_two_elements_higher_same(self):
        key = (15, 8)
        expected = [(12, 8), (13, 8), (14, 8), (15, 8)]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((15, 8), self.keeper._keyMax)

    def test_two_elements_higher_higher(self):
        key = (15, 13)
        expected = [
            (11, 9), (11, 10), (11, 11), (11, 12), (11, 13),
            (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13),
            (13, 8), (13, 9), (13, 10), (13, 11), (13, 12), (13, 13),
            (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13),
            (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (15, 13),
            ]
        self.assertEqual(expected, self.keeper.update(key))
        self.assertEqual((15, 13), self.keeper._keyMax)

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
        counter = Counter.Counter(('var', ), MockKeyComposer(), counts, MockWeightCalculator())
        counter.event(MockEvent())
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([ ], counts._keys)

        counter.event(MockEvent())
        self.assertEqual([((11, ), 1.0), ((13, ), 1.0)], counts._counts)
        self.assertEqual([(12,), (13,)], counts._keys)

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
