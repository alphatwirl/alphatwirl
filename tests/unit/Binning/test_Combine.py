from AlphaTwirl.Binning import Combine, Round, RoundLog
import unittest

##____________________________________________________________________________||
def plus2(val): return val + 2

##____________________________________________________________________________||
class TestCombine(unittest.TestCase):
    def test_call(self):
        low = Round(20.0, 100)
        high = RoundLog(0.1, 100)
        binning = Combine(low =low, high = high, at = 100)
        self.assertEqual(0, binning(10))
        self.assertEqual(80, binning(90))
        self.assertEqual(100, binning(100))

    def test_next(self):
        low = Round(20.0, 100)
        high = RoundLog(0.1, 100)
        binning = Combine(low =low, high = high, at = 100)
        self.assertEqual(20, binning.next(10))
        self.assertEqual(100, binning.next(90))
        self.assertEqual(125.89254117941675, binning.next(100))

##____________________________________________________________________________||
