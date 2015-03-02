from AlphaTwirl.Binning import Binning, Echo, Round
import unittest

##____________________________________________________________________________||
class TestBinning(unittest.TestCase):
    def test_call(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        binning = Binning(bins = bins, lows = lows, ups = ups)
        self.assertEqual(1, binning(15))
        self.assertEqual(2, binning(21))
        self.assertEqual(2, binning(20)) # on the low edge
        self.assertEqual(0, binning(5)) # underflow
        self.assertEqual(5, binning(55)) # overflow

    def test_call_with_list(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        binning = Binning(bins = bins, lows = lows, ups = ups)
        self.assertEqual([1, 2, 2, 0, 5], binning((15, 21, 20, 5, 55)))
        self.assertEqual([1, 2, 2, 0, 5], binning([15, 21, 20, 5, 55]))
        self.assertEqual([1, [3, 2], 2, 0, 5], binning([15, (32, 22), 20, 5, 55]))

    def test_onBoundary(self):
        boundaries = (0.000001, 0.00001, 0.0001)
        binning = Binning(boundaries = boundaries)
        self.assertEqual([1, 2, 3], binning((0.000001, 0.00001, 0.0001)))

    def test_lowedge(self):
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        binning = Binning(lows = lows, ups = ups, retvalue = 'lowedge')
        self.assertEqual([10, 20, 20, float("-inf"), 50], binning((15, 21, 20, 5, 55)))

    def test_init_retvalue(self):
        boundaries = (10, 20, 30, 40, 50)
        Binning(boundaries = boundaries)
        Binning(boundaries = boundaries, retvalue = 'number')
        Binning(boundaries = boundaries, retvalue = 'lowedge')
        self.assertRaises(ValueError, Binning, boundaries = boundaries, retvalue = 'center')
        self.assertRaises(ValueError, Binning, boundaries = boundaries, retvalue = 'yyy')

        self.assertRaises(ValueError, Binning, boundaries = boundaries, retvalue = 'lowedge', bins = (1, 2, 3, 4))
        self.assertRaises(ValueError, Binning, boundaries = boundaries, retvalue = 'lowedge', underflow_bin = -1)
        self.assertRaises(ValueError, Binning, boundaries = boundaries, retvalue = 'lowedge', overflow_bin = -1)

    def test_init_with_bins_lows_ups(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(bins = bins, lows = lows, ups = ups)
        self.assertEqual(bins, binning.bins)
        self.assertEqual(boundaries, binning.boundaries)

    def test_init_with_lows_ups(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(lows = lows, ups = ups)
        self.assertEqual(bins, binning.bins)
        self.assertEqual(boundaries, binning.boundaries)

    def test_init_with_boundaries(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(boundaries = boundaries)
        self.assertEqual(bins, binning.bins)
        self.assertEqual(lows, binning.lows)
        self.assertEqual(ups, binning.ups)

    def test_init_exceptions(self):
        self.assertRaises(ValueError, Binning)
        self.assertRaises(ValueError, Binning, lows = 1)
        self.assertRaises(ValueError, Binning, ups = 1)
        self.assertRaises(ValueError, Binning, boundaries = 1, lows = 1)
        self.assertRaises(ValueError, Binning, boundaries = 1, ups = 1)
        self.assertRaises(ValueError, Binning, boundaries = 1, lows = 1, ups = 1)

        lows = (10.0, 20.0, 30.0, 45.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        self.assertRaises(ValueError, Binning, lows = lows, ups = ups)

    def test_init_exceptions_nobin(self):
        boundaries = (10, )
        self.assertRaises(ValueError, Binning, boundaries = boundaries)

    def test_next_number(self):
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(boundaries = boundaries)
        self.assertEqual([1, 2, 3, 4, 5, 5], binning.next((0, 1, 2, 3, 4, 5)))

        self.assertEqual(5, binning.next(5)) # overflow_bin returns the same

        self.assertRaises(ValueError, binning.next, 2.5)
        self.assertRaises(ValueError, binning.next, 6)

    def test_next_lowedge(self):
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(boundaries = boundaries, retvalue = 'lowedge')
        self.assertEqual([20, 30, 40, 50, 50], binning.next((10, 20, 30, 40, 50))) # on the boundaries

        self.assertEqual(10, binning.next(float('-inf'))) # underflow_bin

        boundaries = (0.001, 0.002, 0.003, 0.004, 0.005)
        binning = Binning(boundaries = boundaries, retvalue = 'lowedge')
        self.assertEqual([0.002, 0.003, 0.004, 0.005, 0.005], binning.next((0.001, 0.002, 0.003, 0.004, 0.005)))

##____________________________________________________________________________||
class TestRound(unittest.TestCase):

    def test_init(self):
        self.assertRaises(ValueError, Binning, boundaries = 1, lows = 1, ups = 1)
        Round(retvalue = 'center')
        Round(retvalue = 'lowedge')
        self.assertRaises(ValueError, Round, retvalue = 'yyy')

    def test_boundary(self):
        self.assertEqual(0.5, Round().aBoundary)
        self.assertEqual(1, Round(2).aBoundary)
        self.assertEqual(5, Round(10).aBoundary)
        self.assertEqual(0, Round(2, 0).aBoundary)
        self.assertEqual(1.5, Round(2, -0.5).aBoundary)
        self.assertEqual(0.5, Round(2, 0.5).aBoundary)
        self.assertEqual(1.5, Round(2, 19.5).aBoundary)
        self.assertEqual(0.5, Round(2, 20.5).aBoundary)
        self.assertEqual(1.5, Round(2, -2.5).aBoundary)
        self.assertEqual(1.5, Round(2, -20.5).aBoundary)

    def test_shift(self):
        self.assertEqual(0, Round(2).shift)
        self.assertEqual(1, Round(2, 0).shift)
        self.assertEqual(1, Round(2, 2).shift)
        self.assertEqual(1, Round(2, 20).shift)
        self.assertEqual(1, Round(2, -20).shift)
        self.assertEqual(0.5, Round(2, 0.5).shift)
        self.assertEqual(0.5, Round(2, 2.5).shift)
        self.assertEqual(0.5, Round(2, 4.5).shift)

    def test_call(self):
        binning = Round()
        self.assertEqual(1, binning(0.5))
        self.assertEqual(1, binning(1.4))
        self.assertEqual(105, binning(104.5))
        self.assertEqual(0, binning(-0.4))
        self.assertEqual(0, binning(-0.5))
        self.assertEqual(-1, binning(-1.4))
        self.assertEqual(-1, binning(-1.5))
        self.assertEqual(-2, binning(-1.6))

    def test_call_with_list(self):
        binning = Round()
        self.assertEqual([1, 1, 105, 0, 0, -1, -1], binning((0.5, 1.4, 104.5, -0.4, -0.5, -1.4, -1.5 )))

    def test_call_width_2(self):
        binning = Round(2)
        self.assertEqual(1, binning.aBoundary)
        self.assertEqual([-2, -2, -2, 0, 0, 0, 2, 2, 2], binning((-2.9, -2, -1.1, -0.9, 0, 0.9, 1.1, 2, 2.9)))

    def test_call_width_2_aboundary_0(self):
        binning = Round(2, 0)
        self.assertEqual(0, binning.aBoundary)
        self.assertEqual([-1, -1, -1, 1, 1, 1, 3, 3, 3], binning((-1.9, -1, -0.1, 0.1, 1, 1.9, 2.1, 3, 3.9)))

    def test_call_decimal_width(self):
        binning = Round(0.02, 0.005)
        self.assertEqual([0.015, 0.035, 0.075, -0.045, -0.005], binning((0.005, 0.025, 0.081, -0.048, -0.015)))

    def test_lowedge(self):
        binning = Round(retvalue = 'lowedge')
        self.assertEqual([0.5, 0.5, 104.5, -0.5, -1.5, -1.5, -1.5], binning((0.51, 1.41, 104.6, -0.4, -0.51, -1.4, -1.5 )))

        binning = Round(0.02, 0.005, retvalue = 'lowedge')
        self.assertEqual([0.005, 0.025, 0.065, -0.055, -0.015], binning((0.005, 0.025, 0.081, -0.048, -0.015)))

    def test_onBoundary(self):
        binning = Round()
        self.assertEqual([-1, 0, 1, 2], binning((-1.5, -0.5, 0.5, 1.5)))

        binning = Round(retvalue = 'lowedge')
        self.assertEqual([-1.5, -0.5, 0.5, 1.5], binning((-1.5, -0.5, 0.5, 1.5)))

        binning = Round(0.02, 0.005)
        self.assertEqual([-0.025, -0.005, 0.015, 0.035, 0.055], binning((-0.035, -0.015, 0.005, 0.025, 0.045)))

        binning = Round(0.02, 0.005, retvalue = 'lowedge')
        self.assertEqual([-0.035, -0.015, 0.005, 0.025, 0.045], binning((-0.035, -0.015, 0.005, 0.025, 0.045)))

    def test_next(self):
        binning = Round()
        self.assertEqual([0, 1, 2, 3], binning.next([-1, 0, 1, 2]))

        binning = Round(retvalue = 'lowedge')
        self.assertEqual([-0.5, 0.5, 1.5, 2.5], binning.next([-1.5, -0.5, 0.5, 1.5]))

        binning = Round(0.02, 0.005)
        self.assertEqual([-0.005, 0.015, 0.035, 0.055, 0.075], binning.next([-0.025, -0.005, 0.015, 0.035, 0.055]))

        binning = Round(0.02, 0.005, retvalue = 'lowedge')
        self.assertEqual([-0.015, 0.005, 0.025, 0.045, 0.065], binning.next([-0.035, -0.015, 0.005, 0.025, 0.045]))

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
