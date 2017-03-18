import unittest

from alphatwirl.binning import Binning

##__________________________________________________________________||
class TestBinning(unittest.TestCase):
    def test_call(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        obj = Binning(bins = bins, lows = lows, ups = ups, retvalue = 'number')
        self.assertEqual(1, obj(15))
        self.assertEqual(2, obj(21))
        self.assertEqual(2, obj(20)) # on the low edge
        self.assertEqual(0, obj(5)) # underflow
        self.assertEqual(5, obj(55)) # overflow

    def test_onBoundary(self):
        boundaries = (0.000001, 0.00001, 0.0001)
        obj = Binning(boundaries = boundaries, retvalue = 'number')
        self.assertEqual( 1, obj( 0.000001 ))
        self.assertEqual( 2, obj( 0.00001  ))
        self.assertEqual( 3, obj( 0.0001   ))

    def test_lowedge(self):
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        obj = Binning(lows = lows, ups = ups, retvalue = 'lowedge')
        self.assertEqual(            10, obj( 15 ))
        self.assertEqual(            20, obj( 21 ))
        self.assertEqual(            20, obj( 20 ))
        self.assertEqual( float("-inf"), obj(  5 ))
        self.assertEqual(            50, obj( 55 ))

        obj = Binning(lows = lows, ups = ups) # 'lowedge' is default
        self.assertEqual(            10, obj( 15 ))
        self.assertEqual(            20, obj( 21 ))
        self.assertEqual(            20, obj( 20 ))
        self.assertEqual( float("-inf"), obj(  5 ))
        self.assertEqual(            50, obj( 55 ))


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
        obj = Binning(bins = bins, lows = lows, ups = ups, retvalue = 'number')
        self.assertEqual(bins, obj.bins)
        self.assertEqual(boundaries, obj.boundaries)

    def test_init_with_lows_ups(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        obj = Binning(lows = lows, ups = ups, retvalue = 'number')
        self.assertEqual(bins, obj.bins)
        self.assertEqual(boundaries, obj.boundaries)


    def test_init_with_boundaries(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        obj = Binning(boundaries = boundaries, retvalue = 'number')
        self.assertEqual(bins, obj.bins)
        self.assertEqual(lows, obj.lows)
        self.assertEqual(ups, obj.ups)


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
        obj = Binning(boundaries = boundaries, retvalue = 'number')
        self.assertEqual( 1, obj.next(0))
        self.assertEqual( 2, obj.next(1))
        self.assertEqual( 3, obj.next(2))
        self.assertEqual( 4, obj.next(3))
        self.assertEqual( 5, obj.next(4))
        self.assertEqual( 5, obj.next(5))

        self.assertEqual(5, obj.next(5)) # overflow_bin returns the same

        self.assertRaises(ValueError, obj.next, 2.5)
        self.assertRaises(ValueError, obj.next, 6)

    def test_next_lowedge(self):
        boundaries = (10, 20, 30, 40, 50)
        obj = Binning(boundaries = boundaries, retvalue = 'lowedge')

        # on the boundaries
        self.assertEqual( 20, obj.next(10))
        self.assertEqual( 30, obj.next(20))
        self.assertEqual( 40, obj.next(30))
        self.assertEqual( 50, obj.next(40))
        self.assertEqual( 50, obj.next(50))

        # underflow_bin
        self.assertEqual(10, obj.next(float('-inf')))

        boundaries = (0.001, 0.002, 0.003, 0.004, 0.005)
        obj = Binning(boundaries = boundaries, retvalue = 'lowedge')
        self.assertEqual( 0.002, obj.next( 0.001))
        self.assertEqual( 0.003, obj.next( 0.002))
        self.assertEqual( 0.004, obj.next( 0.003))
        self.assertEqual( 0.005, obj.next( 0.004))
        self.assertEqual( 0.005, obj.next( 0.005))

    def test_valid(self):
        obj = Binning(boundaries = (30, 40, 50), retvalue = 'number', valid = lambda x: x >= 10)
        self.assertEqual( 1, obj( 33))
        self.assertEqual( 2, obj( 45))
        self.assertIsNone(obj( 9))

##__________________________________________________________________||
