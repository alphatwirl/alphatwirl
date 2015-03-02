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
