import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockBinning(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##____________________________________________________________________________||
class TestKeyMaxKeeper(unittest.TestCase):

    def setUp(self):
        self.binnings = (MockBinning(), MockBinning())
        self.keeper = Counter.KeyMaxKeeper(self.binnings)
        self.keeper.update((11, 8))

    def test_None_at_beginning(self):
        keyMax = Counter.KeyMaxKeeper((MockBinning(), ))
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

    def test_next(self):
        binnings = (MockBinning(), MockBinning())
        keeper = Counter.KeyMaxKeeper(self.binnings)
        self.assertEqual((12, 9), keeper.next((11, 8)))

##____________________________________________________________________________||
class TestKeyMinMaxKeeper(unittest.TestCase):

    def test_None_at_beginning(self):
        keeper = Counter.KeyMinMaxKeeper((MockBinning(), ))
        self.assertIsNone(keeper._keyMin)
        self.assertIsNone(keeper._keyMax)

    def test_the_first_update(self):
        keeper = Counter.KeyMinMaxKeeper((MockBinning(), ))
        self.assertEqual([ ], keeper.update((11, )))
        self.assertEqual((11, ), keeper._keyMin)
        self.assertEqual((11, ), keeper._keyMax)

    def test_two_elements(self):
        keeper = Counter.KeyMinMaxKeeper((MockBinning(), MockBinning()))
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

    def test_next(self):
        binnings = (MockBinning(), MockBinning())
        keeper = Counter.KeyMinMaxKeeper(binnings)
        self.assertEqual((12, 9), keeper.next((11, 8)))

##____________________________________________________________________________||
class TestKeyMaxKeeperBuilder(unittest.TestCase):

    def test_call(self):
        binnings = (MockBinning(), )
        builder = Counter.KeyMaxKeeperBuilder(binnings)
        keeper1 = builder()
        keeper2 = builder()
        self.assertIsInstance(keeper1, Counter.KeyMaxKeeper)
        self.assertIsInstance(keeper2, Counter.KeyMaxKeeper)
        self.assertEqual(keeper1._binnings, binnings)
        self.assertIsNot(keeper1, keeper2)

##____________________________________________________________________________||
