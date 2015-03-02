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
    def __init__(self):
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

    def test_events(self):
        counts = MockCounts()
        keys = [(14, ), (11, )]
        keycomposer = MockKeyComposer(keys)
        counter = Counter.Counter(('var', ), keycomposer, counts, MockWeightCalculator())
        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts.results())


    def test_keynames(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        self.assertEqual(('var', ), counter.keynames())

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGap(unittest.TestCase):

    def test_count(self):
        counts = MockCounts()
        keys = [(14, ), (11, )]
        keyMaxKeeper = MockKeyMaxKeeper()
        keyMaxKeeper.updates = [[(11, ), (12, ), (13, ), (14, )], [()]]
        countsWEKIG = Counter.CountsWithEmptyKeysInGap(counts, keyMaxKeeper)

        countsWEKIG.count((11, ), 1)
        self.assertEqual([(11,)], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0)], counts._counts)
        self.assertEqual([[()]], counts._keys)

        countsWEKIG.count((14, ), 1)
        self.assertEqual([(11, ), (14, )], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([[()], [(11, ), (12, ), (13, ), (14, )]], counts._keys)

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGapBulder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CountsWithEmptyKeysInGapBulder(MockCounts, MockKeyMaxKeeper)
        counts1 = builder()
        counts2 = builder()
        self.assertIsInstance(counts1, Counter.CountsWithEmptyKeysInGap)
        self.assertIsInstance(counts1._countMethod, MockCounts)
        self.assertIsInstance(counts1._keyMaxKeeper, MockKeyMaxKeeper)
        self.assertIsNot(counts1, counts2)
        self.assertIsNot(counts1._countMethod, counts2._countMethod)
        self.assertIsNot(counts1._keyMaxKeeper, counts2._keyMaxKeeper)

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
