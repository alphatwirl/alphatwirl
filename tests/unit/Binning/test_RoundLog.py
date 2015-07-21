from AlphaTwirl.Binning import RoundLog
import unittest

##____________________________________________________________________________||
class TestRoundLog(unittest.TestCase):

    def test_init(self):
        RoundLog(retvalue = 'center')
        RoundLog(retvalue = 'lowedge')
        self.assertRaises(ValueError, RoundLog, retvalue = 'yyy')

    def test_call(self):
        binning = RoundLog()
        self.assertAlmostEqual( 1.9952623149688, binning(   2))
        self.assertAlmostEqual( 19.952623149688, binning(  20))
        self.assertAlmostEqual( 199.52623149688, binning( 200))

    def test_call_center(self):
        binning = RoundLog(retvalue = 'center')
        self.assertAlmostEqual( 2.23872113856834, binning(   2))
        self.assertAlmostEqual( 22.3872113856834, binning(  20))
        self.assertAlmostEqual( 223.872113856834, binning( 200))

    def test_next(self):
        binning = RoundLog(retvalue = 'center')
        self.assertAlmostEqual( 2.818382931264, binning.next(2.23872113856834))
        self.assertAlmostEqual( 28.18382931264, binning.next(22.3872113856834))
        self.assertAlmostEqual( 281.8382931264, binning.next(223.872113856834))

    def test_call_zero(self):
        binning = RoundLog()
        self.assertIsNone(binning(0))

    def test_call_negative(self):
        binning = RoundLog()
        self.assertIsNone(binning(-1))

    def test_valid(self):
        binning = RoundLog(valid = lambda x: x >= 10)
        self.assertAlmostEqual( 12.589254117941675, binning(13))
        self.assertAlmostEqual( 10.0, binning(10))
        self.assertIsNone(binning(7))

    def test_onBoundary(self):
        binning = RoundLog(0.1, 100)
        self.assertEqual( 100, binning( 100))

##____________________________________________________________________________||
