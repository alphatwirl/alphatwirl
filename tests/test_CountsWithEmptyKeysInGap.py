import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockCounts(object):
    def __init__(self):
        self._counts = [ ]
        self._keys = [ ]

    def count(self, key, weight):
        self._counts.append((key, weight))

    def addKeys(self, keys):
        self._keys.append(keys)

##____________________________________________________________________________||
class MockKeyMaxKeeper(object):
    def __init__(self):
        self.keys = [ ]
        self.updates = [ ]
        self.nexts = [ ]

    def update(self, key):
        self.keys.append(key)
        return self.updates.pop()

    def next(self, key):
        return self.nexts.pop()

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
class TestCountsWithEmptyKeysInGapAndNext(unittest.TestCase):

    def test_count(self):
        counts = MockCounts()
        keyMaxKeeper = MockKeyMaxKeeper()
        countsWEKIG = Counter.CountsWithEmptyKeysInGapAndNext(counts, keyMaxKeeper)

        keyMaxKeeper.updates = [[()], [()]]
        keyMaxKeeper.nexts = [(12, )]
        countsWEKIG.count((11, ), 1)
        self.assertEqual([(11,), (12,)], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0)], counts._counts)
        self.assertEqual([[()]], counts._keys)

        keyMaxKeeper.updates = [[(12, ), (13, ), (14, ), (15, )]]
        keyMaxKeeper.nexts = [(15, )]
        countsWEKIG.count((14, ), 1)
        self.assertEqual([(11, ), (12, ), (15, )], keyMaxKeeper.keys)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([[()], [(12, ), (13, ), (14, ), (15, )]], counts._keys)

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGapBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CountsWithEmptyKeysInGapBuilder(MockCounts, MockKeyMaxKeeper)
        counts1 = builder()
        counts2 = builder()
        self.assertIsInstance(counts1, Counter.CountsWithEmptyKeysInGap)
        self.assertIsInstance(counts1._countMethod, MockCounts)
        self.assertIsInstance(counts1._keyMaxKeeper, MockKeyMaxKeeper)
        self.assertIsNot(counts1, counts2)
        self.assertIsNot(counts1._countMethod, counts2._countMethod)
        self.assertIsNot(counts1._keyMaxKeeper, counts2._keyMaxKeeper)

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGapAndNextBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CountsWithEmptyKeysInGapAndNextBuilder(MockCounts, MockKeyMaxKeeper)
        counts1 = builder()
        counts2 = builder()
        self.assertIsInstance(counts1, Counter.CountsWithEmptyKeysInGapAndNext)
        self.assertIsInstance(counts1._countMethod, MockCounts)
        self.assertIsInstance(counts1._keyMaxKeeper, MockKeyMaxKeeper)
        self.assertIsNot(counts1, counts2)
        self.assertIsNot(counts1._countMethod, counts2._countMethod)
        self.assertIsNot(counts1._keyMaxKeeper, counts2._keyMaxKeeper)

##____________________________________________________________________________||
