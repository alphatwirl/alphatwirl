import unittest

from AlphaTwirl.Binning import Round

##__________________________________________________________________||
class TestRound(unittest.TestCase):

    def test_init(self):
        Round(retvalue = 'center')
        Round(retvalue = 'lowedge')
        self.assertRaises(ValueError, Round, retvalue = 'yyy')

    def test__repr(self):
        obj = Round()
        repr(obj)

    def test_call(self):
        obj = Round()
        self.assertEqual(0.5, obj(0.5))
        self.assertEqual(0.5, obj(1.4))
        self.assertEqual(104.5, obj(104.5))
        self.assertEqual(-0.5, obj(-0.4))
        self.assertEqual(-0.5, obj(-0.5))
        self.assertEqual(-1.5, obj(-1.4))
        self.assertEqual(-1.5, obj(-1.5))
        self.assertEqual(-2.5, obj(-1.6))

    def test_call_width_2(self):
        obj = Round(2)
        self.assertEqual( -3, obj( -2.9))
        self.assertEqual( -3, obj( -2  ))
        self.assertEqual( -3, obj( -1.1))
        self.assertEqual( -1, obj( -0.9))
        self.assertEqual( -1, obj(  0  ))
        self.assertEqual( -1, obj(  0.9))
        self.assertEqual(  1, obj(  1.1))
        self.assertEqual(  1, obj(  2  ))
        self.assertEqual(  1, obj(  2.9))

    def test_call_width_2_aboundary_0(self):
        obj = Round(2, 0)
        self.assertEqual( -2, obj( -1.9))
        self.assertEqual( -2, obj( -1  ))
        self.assertEqual( -2, obj( -0.1))
        self.assertEqual(  0, obj(  0.1))
        self.assertEqual(  0, obj(  1  ))
        self.assertEqual(  0, obj(  1.9))
        self.assertEqual(  2, obj(  2.1))
        self.assertEqual(  2, obj(  3  ))
        self.assertEqual(  2, obj(  3.9))

    def test_call_decimal_width(self):
        obj = Round(0.02, 0.005)
        self.assertAlmostEqual(  0.005, obj(  0.005))
        self.assertAlmostEqual(  0.025, obj(  0.025))
        self.assertAlmostEqual(  0.065, obj(  0.081))
        self.assertAlmostEqual( -0.055, obj( -0.048))
        self.assertAlmostEqual( -0.015, obj( -0.015))

    def test_center(self):
        obj = Round(retvalue = 'center')
        self.assertEqual(   1.0, obj(   0.51))
        self.assertEqual(   1.0, obj(   1.41))
        self.assertEqual( 105.0, obj( 104.6 ))
        self.assertEqual(  -0.0, obj(  -0.4 ))
        self.assertEqual(  -1.0, obj( -0.51 ))
        self.assertEqual(  -1.0, obj( -1.4  ))
        self.assertEqual(  -1.0, obj( -1.5  ))

        obj = Round(0.02, 0.005, retvalue = 'center')
        self.assertAlmostEqual(  0.015, obj(  0.005))
        self.assertAlmostEqual(  0.035, obj(  0.025))
        self.assertAlmostEqual(  0.075, obj(  0.081))
        self.assertAlmostEqual( -0.045, obj( -0.048))
        self.assertAlmostEqual( -0.005, obj( -0.015))

    def test_onBoundary(self):
        obj = Round()
        self.assertEqual( -1.5, obj( -1.5))
        self.assertEqual( -0.5, obj( -0.5))
        self.assertEqual(  0.5, obj(  0.5))
        self.assertEqual(  1.5, obj(  1.5))

        obj = Round(retvalue = 'center')
        self.assertEqual( -1, obj( -1.5))
        self.assertEqual(  0, obj( -0.5))
        self.assertEqual(  1, obj(  0.5))
        self.assertEqual(  2, obj(  1.5))

        obj = Round(0.02, 0.005)
        self.assertEqual( -0.035, obj( -0.035))
        self.assertEqual( -0.015, obj( -0.015))
        self.assertEqual(  0.005, obj(  0.005))
        self.assertEqual(  0.025, obj(  0.025))
        self.assertEqual(  0.045, obj(  0.045))

        obj = Round(0.02, 0.005, retvalue = 'center')
        self.assertAlmostEqual( -0.025, obj( -0.035))
        self.assertAlmostEqual( -0.005, obj( -0.015))
        self.assertAlmostEqual(  0.015, obj(  0.005))
        self.assertAlmostEqual(  0.035, obj(  0.025))
        self.assertAlmostEqual(  0.055, obj(  0.045))

    def test_next(self):
        obj = Round()
        self.assertEqual( -0.5, obj.next( -1.5))
        self.assertEqual(  0.5, obj.next( -0.5))
        self.assertEqual(  1.5, obj.next(  0.5))
        self.assertEqual(  2.5, obj.next(  1.5))

        obj = Round(retvalue = 'center')
        self.assertEqual( 0, obj.next( -1))
        self.assertEqual( 1, obj.next(  0))
        self.assertEqual( 2, obj.next(  1))
        self.assertEqual( 3, obj.next(  2))

        obj = Round(0.02, 0.005)
        self.assertEqual( -0.015, obj.next( -0.035))
        self.assertEqual(  0.005, obj.next( -0.015))
        self.assertEqual(  0.025, obj.next(  0.005))
        self.assertEqual(  0.045, obj.next(  0.025))
        self.assertEqual(  0.065, obj.next(  0.045))

        obj = Round(0.02, 0.005, retvalue = 'center')
        self.assertAlmostEqual( -0.005, obj.next( -0.025))
        self.assertAlmostEqual(  0.015, obj.next( -0.005))
        self.assertAlmostEqual(  0.035, obj.next(  0.015))
        self.assertAlmostEqual(  0.055, obj.next(  0.035))
        self.assertAlmostEqual(  0.075, obj.next(  0.055))

    def test_valid(self):
        obj = Round(valid = lambda x: x >= 0)
        self.assertEqual(  0.5, obj(  1))
        self.assertEqual( -0.5, obj(  0))
        self.assertEqual( None, obj( -1))

    def test_min(self):
        obj = Round(10, 100, min = 30)
        self.assertEqual(  100, obj( 100))
        self.assertEqual(   30, obj(  30))
        self.assertEqual( None, obj(  29))

    def test_min_underflow_bin(self):
        obj = Round(10, 100, min = 30, underflow_bin = 0)
        self.assertEqual(  100, obj( 100))
        self.assertEqual(   30, obj(  30))
        self.assertEqual(    0, obj(  29))

        self.assertEqual( obj(30), obj.next( 0)) # the next to the underflow
                                                 # bin is the bin for the min

    def test_max(self):
        obj = Round(10, 100, max = 150)
        self.assertEqual(  100, obj( 100))
        self.assertEqual( None, obj( 150))
        self.assertEqual( None, obj( 500))

    def test_max_overflow_bin(self):
        obj = Round(10, 100, max = 150, overflow_bin = 150)
        self.assertEqual(  100, obj( 100))
        self.assertEqual(  150, obj( 150))
        self.assertEqual(  150, obj( 500))

        self.assertEqual( 150, obj.next(150)) # the next to the overflow
                                              # bin is the overflow bin

    def test_inf(self):
        obj = Round(10, 100)
        self.assertIsNone(obj(float('inf')))
        self.assertIsNone(obj(float('-inf')))
        self.assertIsNone(obj.next(float('inf')))
        self.assertIsNone(obj.next(float('-inf')))
##__________________________________________________________________||
