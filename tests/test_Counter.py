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
        self._keys.append(keys)

    def results(self):
        return self._counts

##____________________________________________________________________________||
class MockKeyMaxKeeper(object):
    def __init__(self, binnings):
        self.keys = [ ]
        self.updates = [ ]
        pass

    def update(self, key):
        self.keys.append(key)
        return self.updates.pop()

##____________________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class MockKeyComposer(object):
    def __init__(self, keys = [ ]):
        self.keys = keys
        self.binning = MockBinning()

    def __call__(self, event):
        return self.keys.pop()

    def binnings(self):
        return (self.binning, )

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

    def test_results(self):
        counts = MockCounts()
        keys = [(11, )]
        keycomposer = MockKeyComposer(keys)
        counter = Counter.Counter(('var', ), keycomposer, counts, MockWeightCalculator())
        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

    def test_keynames(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        self.assertEqual(('var', ), counter.keynames())

    def test_addKeys(self):
        counts = MockCounts()
        keys = [(14, ), (11, )]
        keyComposer = MockKeyComposer(keys)
        keyMaxKeeper = MockKeyMaxKeeper(keyComposer.binnings())
        keyMaxKeeper.updates = [[(11, ), (12, ), (13, ), (14, )], [()]]
        counter = Counter.Counter(('var', ), keyComposer, counts, MockWeightCalculator(), addEmptyKeys = True, keyMaxKeeper = keyMaxKeeper)
        counter.event(MockEvent())
        self.assertEqual([(11,)], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0)], counts._counts)
        self.assertEqual([[()]], counts._keys)

        counter.event(MockEvent())
        self.assertEqual([(11, ), (14, )], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([[()], [(11, ), (12, ), (13, ), (14, )]], counts._keys)

    def test_addKeys_disabled(self):
        counts = MockCounts()
        keys = [(14, ), (11, )]
        keyComposer = MockKeyComposer(keys)
        keyMaxKeeper = MockKeyMaxKeeper(keyComposer.binnings())
        keyMaxKeeper.updates = [[(11, ), (12, ), (13, ), (14, )], [()]]
        counter = Counter.Counter(('var', ), keyComposer, counts, MockWeightCalculator(), addEmptyKeys = False, keyMaxKeeper = keyMaxKeeper)
        counter.event(MockEvent())
        self.assertEqual([ ], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0)], counts._counts)
        self.assertEqual([ ], counts._keys)

        counter.event(MockEvent())
        self.assertEqual([ ], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
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

    def test_addEmptyKeys_default(self):
        builder = Counter.CounterBuilder(('var_bin', ), MockKeyComposer(), MockCounts)
        counter1 = builder()
        self.assertFalse(counter1._addEmptyKeys)

    def test_addEmptyKeys_True(self):
        builder = Counter.CounterBuilder(('var_bin', ), MockKeyComposer(), MockCounts, addEmptyKeys = True)
        counter1 = builder()
        self.assertTrue(counter1._addEmptyKeys)

    def test_addEmptyKeys_False(self):
        builder = Counter.CounterBuilder(('var_bin', ), MockKeyComposer(), MockCounts, addEmptyKeys = False)
        counter1 = builder()
        self.assertFalse(counter1._addEmptyKeys)

    def test_keyMaxKeeper(self):
        builder = Counter.CounterBuilder(('var_bin', ), MockKeyComposer(), MockCounts, addEmptyKeys = True, keyMaxKeeperClass = MockKeyMaxKeeper)
        counter1 = builder()
        self.assertIsInstance(counter1._keyMaxKeeper, MockKeyMaxKeeper)

##____________________________________________________________________________||
