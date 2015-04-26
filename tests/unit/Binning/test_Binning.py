from AlphaTwirl.Binning import Binning
import unittest

##____________________________________________________________________________||
class TestBinning(unittest.TestCase):
    def test_call(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        binning = Binning(bins = bins, lows = lows, ups = ups, retvalue = 'number')
        self.assertEqual(1, binning(15))
        self.assertEqual(2, binning(21))
        self.assertEqual(2, binning(20)) # on the low edge
        self.assertEqual(0, binning(5)) # underflow
        self.assertEqual(5, binning(55)) # overflow

    def test_onBoundary(self):
        boundaries = (0.000001, 0.00001, 0.0001)
        binning = Binning(boundaries = boundaries, retvalue = 'number')
        self.assertEqual( 1, binning( 0.000001 ))
        self.assertEqual( 2, binning( 0.00001  ))
        self.assertEqual( 3, binning( 0.0001   ))

    def test_lowedge(self):
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        binning = Binning(lows = lows, ups = ups, retvalue = 'lowedge')
        self.assertEqual(            10, binning( 15 ))
        self.assertEqual(            20, binning( 21 ))
        self.assertEqual(            20, binning( 20 ))
        self.assertEqual( float("-inf"), binning(  5 ))
        self.assertEqual(            50, binning( 55 ))

        binning = Binning(lows = lows, ups = ups) # 'lowedge' is default
        self.assertEqual(            10, binning( 15 ))
        self.assertEqual(            20, binning( 21 ))
        self.assertEqual(            20, binning( 20 ))
        self.assertEqual( float("-inf"), binning(  5 ))
        self.assertEqual(            50, binning( 55 ))


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
        binning = Binning(bins = bins, lows = lows, ups = ups, retvalue = 'number')
        self.assertEqual(bins, binning.bins)
        self.assertEqual(boundaries, binning.boundaries)

    def test_init_with_lows_ups(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(lows = lows, ups = ups, retvalue = 'number')
        self.assertEqual(bins, binning.bins)
        self.assertEqual(boundaries, binning.boundaries)


    def test_init_with_boundaries(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(boundaries = boundaries, retvalue = 'number')
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
        binning = Binning(boundaries = boundaries, retvalue = 'number')
        self.assertEqual( 1, binning.next(0))
        self.assertEqual( 2, binning.next(1))
        self.assertEqual( 3, binning.next(2))
        self.assertEqual( 4, binning.next(3))
        self.assertEqual( 5, binning.next(4))
        self.assertEqual( 5, binning.next(5))

        self.assertEqual(5, binning.next(5)) # overflow_bin returns the same

        self.assertRaises(ValueError, binning.next, 2.5)
        self.assertRaises(ValueError, binning.next, 6)

    def test_next_lowedge(self):
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(boundaries = boundaries, retvalue = 'lowedge')

        # on the boundaries
        self.assertEqual( 20, binning.next(10))
        self.assertEqual( 30, binning.next(20))
        self.assertEqual( 40, binning.next(30))
        self.assertEqual( 50, binning.next(40))
        self.assertEqual( 50, binning.next(50))

        # underflow_bin
        self.assertEqual(10, binning.next(float('-inf')))

        boundaries = (0.001, 0.002, 0.003, 0.004, 0.005)
        binning = Binning(boundaries = boundaries, retvalue = 'lowedge')
        self.assertEqual( 0.002, binning.next( 0.001))
        self.assertEqual( 0.003, binning.next( 0.002))
        self.assertEqual( 0.004, binning.next( 0.003))
        self.assertEqual( 0.005, binning.next( 0.004))
        self.assertEqual( 0.005, binning.next( 0.005))

    def test_valid(self):
        binning = Binning(boundaries = (30, 40, 50), retvalue = 'number', valid = lambda x: x >= 10)
        self.assertEqual( 1, binning( 33))
        self.assertEqual( 2, binning( 45))
        self.assertIsNone(binning( 9))

##____________________________________________________________________________||
