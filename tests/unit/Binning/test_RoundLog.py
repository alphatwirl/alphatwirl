import unittest

from AlphaTwirl.Binning import RoundLog

##__________________________________________________________________||
class TestRoundLog(unittest.TestCase):

    def test_init(self):
        RoundLog(retvalue = 'center')
        RoundLog(retvalue = 'lowedge')
        self.assertRaises(ValueError, RoundLog, retvalue = 'yyy')

    def test_call(self):
        obj = RoundLog()
        self.assertAlmostEqual( 1.9952623149688, obj(   2))
        self.assertAlmostEqual( 19.952623149688, obj(  20))
        self.assertAlmostEqual( 199.52623149688, obj( 200))

    def test_call_center(self):
        obj = RoundLog(retvalue = 'center')
        self.assertAlmostEqual( 2.23872113856834, obj(   2))
        self.assertAlmostEqual( 22.3872113856834, obj(  20))
        self.assertAlmostEqual( 223.872113856834, obj( 200))

    def test_next(self):
        obj = RoundLog(retvalue = 'center')
        self.assertAlmostEqual( 2.818382931264, obj.next(2.23872113856834))
        self.assertAlmostEqual( 28.18382931264, obj.next(22.3872113856834))
        self.assertAlmostEqual( 281.8382931264, obj.next(223.872113856834))

    def test_call_zero(self):
        obj = RoundLog()
        self.assertIsNone(obj(0))

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

##__________________________________________________________________||
