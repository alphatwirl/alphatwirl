#!/usr/bin/env python
from alphatwirl import Binning
import unittest

##____________________________________________________________________________||
class TestBinning(unittest.TestCase):
    def test_call(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        binning = Binning(bins = bins, lows = lows, ups = ups)
        self.assertEqual(binning(15), 1)
        self.assertEqual(binning(21), 2)
        self.assertEqual(binning(20), 2) # on the low edge
        self.assertEqual(binning(5), 0) # underflow
        self.assertEqual(binning(55), 5) # overflow

    def test_call_with_list(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        binning = Binning(bins = bins, lows = lows, ups = ups)
        self.assertEqual(binning((15, 21, 20, 5, 55)), [1, 2, 2, 0, 5])
        self.assertEqual(binning([15, 21, 20, 5, 55]), [1, 2, 2, 0, 5])
        self.assertEqual(binning([15, (32, 22), 20, 5, 55]), [1, [3, 2], 2, 0, 5])

    def test_init_with_bins_lows_ups(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(bins = bins, lows = lows, ups = ups)
        self.assertEqual(binning.bins , bins)
        self.assertEqual(binning.boundaries, boundaries)

    def test_init_with_lows_ups(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(lows = lows, ups = ups)
        self.assertEqual(binning.bins , bins)
        self.assertEqual(binning.boundaries, boundaries)

    def test_init_with_boundaries(self):
        bins = (1, 2, 3, 4)
        lows = (10.0, 20.0, 30.0, 40.0)
        ups = (20.0, 30.0, 40.0, 50.0)
        boundaries = (10, 20, 30, 40, 50)
        binning = Binning(boundaries = boundaries)
        self.assertEqual(binning.bins , bins)
        self.assertEqual(binning.lows , lows)
        self.assertEqual(binning.ups , ups)

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

##____________________________________________________________________________||
