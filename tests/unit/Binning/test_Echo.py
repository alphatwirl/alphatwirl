from alphatwirl.binning import Echo
import unittest

##__________________________________________________________________||
def plus2(val): return val + 2

##__________________________________________________________________||
class TestEcho(unittest.TestCase):
    def test_call(self):
        binning = Echo()
        self.assertEqual(1, binning(1))
        self.assertEqual(2, binning(2))
        self.assertEqual(0, binning(0))
        self.assertEqual(5, binning(5))

    def test_next_default(self):
        binning = Echo()
        self.assertEqual( -4, binning.next( -5))
        self.assertEqual(  1, binning.next(  0))
        self.assertEqual(  2, binning.next(  1))
        self.assertEqual(  4, binning.next(  3))
        self.assertEqual( 11, binning.next( 10))

    def test_next_plus2(self):
        binning = Echo(nextFunc = plus2)
        self.assertEqual( -3, binning.next( -5))
        self.assertEqual(  2, binning.next(  0))
        self.assertEqual(  3, binning.next(  1))
        self.assertEqual(  5, binning.next(  3))
        self.assertEqual( 12, binning.next( 10))

    def test_next_lambda(self):
        binning = Echo(nextFunc = lambda x: x + 0.1)
        self.assertEqual( -4.9, binning.next( -5))
        self.assertEqual(  0.1, binning.next(  0))
        self.assertEqual(  1.1, binning.next(  1))
        self.assertEqual(  3.1, binning.next(  3))
        self.assertEqual( 10.1, binning.next( 10))

    def test_next_None(self):
        binning = Echo(nextFunc = None)
        self.assertIsNone(binning.next( -5))
        self.assertIsNone(binning.next(  0))
        self.assertIsNone(binning.next(  1))
        self.assertIsNone(binning.next(  3))
        self.assertIsNone(binning.next( 10))

    def test_valid(self):
        binning = Echo(valid = lambda x: x >= 10)
        self.assertEqual( 13, binning(13))
        self.assertEqual( 10, binning(10))
        self.assertIsNone(binning(7))

##__________________________________________________________________||
