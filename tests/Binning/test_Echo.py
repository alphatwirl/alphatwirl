from AlphaTwirl.Binning import Echo
import unittest

##____________________________________________________________________________||
def plus2(val): return val + 2

##____________________________________________________________________________||
class TestEcho(unittest.TestCase):
    def test_call(self):
        binning = Echo()
        self.assertEqual(1, binning(1))
        self.assertEqual(2, binning(2))
        self.assertEqual(0, binning(0))
        self.assertEqual(5, binning(5))

    def test_call_with_list(self):
        binning = Echo()
        self.assertEqual([-5, 0, 1, 3, 10], binning([-5, 0, 1, 3, 10]))
        self.assertEqual([-5, 0, 1, 3, 10], binning((-5, 0, 1, 3, 10)))

    def test_next(self):
        binning = Echo()
        self.assertEqual([-4, 1, 2, 4, 11], binning.next([-5, 0, 1, 3, 10]))

        binning = Echo(nextFunc = plus2)
        self.assertEqual([-3, 2, 3, 5, 12], binning.next([-5, 0, 1, 3, 10]))

        binning = Echo(nextFunc = lambda x: x + 0.1)
        self.assertEqual([-4.9, 0.1, 1.1, 3.1, 10.1], binning.next([-5, 0, 1, 3, 10]))

##____________________________________________________________________________||
