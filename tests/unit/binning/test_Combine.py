from alphatwirl.binning import Combine, Round, RoundLog
import unittest

##__________________________________________________________________||
def plus2(val): return val + 2

##__________________________________________________________________||
class TestCombine(unittest.TestCase):
    def test_call(self):
        low = Round(20.0, 100)
        high = RoundLog(0.1, 100)
        binning = Combine(low =low, high = high, at = 100)
        self.assertEqual(0, binning(10))
        self.assertEqual(80, binning(90))
        self.assertEqual(100, binning(100))

        low = Round(10.0, 50)
        high = RoundLog(0.1, 50)
        binning = Combine(low =low, high = high, at = 50)
        self.assertEqual(10, binning(11))
        self.assertEqual(40, binning(40))
        self.assertAlmostEqual(50, binning(50))

    def test_next(self):
        low = Round(20.0, 100)
        high = RoundLog(0.1, 100)
        binning = Combine(low =low, high = high, at = 100)
        self.assertEqual(20, binning.next(10))
        self.assertEqual(100, binning.next(90))
        self.assertEqual(125.89254117941675, binning.next(100))

        low = Round(10.0, 50)
        high = RoundLog(0.1, 50)
        binning = Combine(low =low, high = high, at = 50)
        self.assertEqual(20, binning.next(10))
        self.assertAlmostEqual(50, binning.next(45))
        self.assertEqual(62.94627058970836, binning.next(50))

##__________________________________________________________________||
