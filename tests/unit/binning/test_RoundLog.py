import unittest

from alphatwirl.binning import RoundLog

##__________________________________________________________________||
class TestRoundLog(unittest.TestCase):

    def test_init(self):
        obj = RoundLog()

    def test_call(self):
        obj = RoundLog()
        self.assertAlmostEqual( 1.9952623149688, obj(   2))
        self.assertAlmostEqual( 19.952623149688, obj(  20))
        self.assertAlmostEqual( 199.52623149688, obj( 200))

    def test_next(self):
        obj = RoundLog()
        self.assertAlmostEqual( 2.51188643150958, obj.next(2.23872113856834))
        self.assertAlmostEqual( 25.11886431509581, obj.next(22.3872113856834))
        self.assertAlmostEqual( 251.18864315095848, obj.next(223.872113856834))

    def test_call_zero(self):
        obj = RoundLog()
        self.assertEqual(0, obj(0))

        self.assertEqual(0, obj.next(0)) # next to 0 is 0 unless 0 is the
                                         # underflow bin

    def test_call_negative(self):
        obj = RoundLog()
        self.assertIsNone(obj(-1))

    def test_valid(self):
        obj = RoundLog(valid = lambda x: x >= 10)
        self.assertAlmostEqual( 12.589254117941675, obj(13))
        self.assertAlmostEqual( 10.0, obj(10))
        self.assertIsNone(obj(7))

    def test_onBoundary(self):
        obj = RoundLog(0.1, 100)
        self.assertEqual( 100, obj( 100))

    def test_min(self):
        obj = RoundLog(0.1, 100, min = 10)
        self.assertEqual(  100, obj( 100))
        self.assertAlmostEqual(   10, obj(  10))
        self.assertEqual( None, obj(   9))

    def test_min_underflow_bin(self):
        obj = RoundLog(0.1, 100, min = 10, underflow_bin = 0)
        self.assertEqual(  100, obj( 100))
        self.assertAlmostEqual(   10, obj(  10))
        self.assertEqual( 0, obj(   9))

        self.assertEqual( obj(10), obj.next( 0)) # the next to the underflow
                                                 # bin is the bin for the min

    def test_max(self):
        obj = RoundLog(0.1, 100, max = 1000)
        self.assertEqual(  100, obj(  100))
        self.assertEqual( None, obj( 1000))
        self.assertEqual( None, obj( 5000))

    def test_max_overflow_bin(self):
        obj = RoundLog(0.1, 100, max = 1000, overflow_bin = 1000)
        self.assertEqual(  100, obj(  100))
        self.assertEqual( 1000, obj( 1000))
        self.assertEqual( 1000, obj( 5000))

        self.assertEqual( 1000, obj.next(1000)) # the next to the overflow bin
                                                # is the overflow bin

    def test_inf(self):
        obj = RoundLog(0.1, 100)
        self.assertIsNone(obj(float('inf')))
        self.assertIsNone(obj(float('-inf')))
        self.assertIsNone(obj.next(float('inf')))
        self.assertIsNone(obj.next(float('-inf')))
##__________________________________________________________________||
