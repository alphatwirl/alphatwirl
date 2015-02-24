#!/usr/bin/env python
from AlphaTwirl import Binning, Echo
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

##____________________________________________________________________________||
class TestEcho(unittest.TestCase):
    def test_call(self):
        binning = Echo()
        self.assertEqual(1, binning(1))
        self.assertEqual(2, binning(2))
        self.assertEqual(0, binning(0))
        self.assertEqual(5, binning(5))

##____________________________________________________________________________||
