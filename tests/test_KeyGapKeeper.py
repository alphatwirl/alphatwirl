import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockBinning(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##____________________________________________________________________________||
class MockBinningWithMax(object):
    def __init__(self, max):
        self._max = max

    def __call__(self, val):
        return val

    def next(self, val):
        if val == self._max: return val
        return val + 1

##____________________________________________________________________________||
class TestKeyGapKeeper(unittest.TestCase):

    def test_None_at_beginning(self):
        keeper = Counter.KeyGapKeeper((MockBinning(), ))
        self.assertIsNone(keeper._keyMin)
        self.assertIsNone(keeper._keyMax)

    def test_the_first_update(self):
        keeper = Counter.KeyGapKeeper((MockBinning(), ))
        self.assertEqual([ ], keeper.update((11, )))
        self.assertEqual((11, ), keeper._keyMin)
        self.assertEqual((11, ), keeper._keyMax)

    def test_two_elements(self):
        keeper = Counter.KeyGapKeeper((MockBinning(), MockBinning()))
        key = (25, 150)
        keyMin = (25, 150)
        keyMax = (25, 150)
        expected = [ ]
        self.assertEqual(expected, keeper.update(key))
        self.assertEqual(keyMin, keeper._keyMin)
        self.assertEqual(keyMax, keeper._keyMax)

        key = (23, 148)
        keyMin = (23, 148)
        keyMax = (25, 150)
        expected = [(23, 148), (23, 149), (23, 150),
                    (24, 148), (24, 149), (24, 150),
                    (25, 148), (25, 149)]
        self.assertEqual(expected, keeper.update(key))
        self.assertEqual(keyMin, keeper._keyMin)
        self.assertEqual(keyMax, keeper._keyMax)

        key = (23, 150)
        keyMin = (23, 148)
        keyMax = (25, 150)
        expected = [ ]
        self.assertEqual(expected, keeper.update(key))
        self.assertEqual(keyMin, keeper._keyMin)
        self.assertEqual(keyMax, keeper._keyMax)

        key = (21, 152)
        keyMin = (21, 148)
        keyMax = (25, 152)
        expected = [(21, 148), (21, 149), (21, 150), (21, 151), (21, 152),
                    (22, 148), (22, 149), (22, 150), (22, 151), (22, 152),
                                                     (23, 151), (23, 152),
                                                     (24, 151), (24, 152),
                                                     (25, 151), (25, 152)]
        self.assertEqual(expected, keeper.update(key))
        self.assertEqual(keyMin, keeper._keyMin)
        self.assertEqual(keyMax, keeper._keyMax)

        key = (24, 146)
        keyMin = (21, 146)
        keyMax = (25, 152)
        expected = [(21, 146), (21, 147),
                    (22, 146), (22, 147),
                    (23, 146), (23, 147),
                    (24, 146), (24, 147),
                    (25, 146), (25, 147)]
        self.assertEqual(expected, keeper.update(key))
        self.assertEqual(keyMin, keeper._keyMin)
        self.assertEqual(keyMax, keeper._keyMax)

    def test_same_next(self):
        keeper = Counter.KeyGapKeeper((MockBinning(), MockBinningWithMax(10)))
        key = (5, 9)
        keyMin = (5, 9)
        keyMax = (5, 9)
        expected = [ ]
        self.assertEqual(expected, keeper.update(key))
        self.assertEqual(keyMin, keeper._keyMin)
        self.assertEqual(keyMax, keeper._keyMax)

        key = (5, 10)
        keyMin = (5, 9)
        keyMax = (5, 10)
        expected = [(5, 10)]
        self.assertEqual(expected, keeper.update(key))
        self.assertEqual(keyMin, keeper._keyMin)
        self.assertEqual(keyMax, keeper._keyMax)



    def test_next(self):
        binnings = (MockBinning(), MockBinning())
        keeper = Counter.KeyGapKeeper(binnings)
        self.assertEqual((12, 9), keeper.next((11, 8)))

##____________________________________________________________________________||
class TestKeyGapKeeperBuilder(unittest.TestCase):

    def test_call(self):
        binnings = (MockBinning(), )
        builder = Counter.KeyGapKeeperBuilder(binnings)
        keeper1 = builder()
        keeper2 = builder()
        self.assertIsInstance(keeper1, Counter.KeyGapKeeper)
        self.assertIsInstance(keeper2, Counter.KeyGapKeeper)
        self.assertEqual(keeper1._binnings, binnings)
        self.assertIsNot(keeper1, keeper2)

##____________________________________________________________________________||
