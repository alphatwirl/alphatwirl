from AlphaTwirl.Binning import Round
import unittest

##__________________________________________________________________||
class TestRound(unittest.TestCase):

    def test_init(self):
        Round(retvalue = 'center')
        Round(retvalue = 'lowedge')
        self.assertRaises(ValueError, Round, retvalue = 'yyy')

    def test_call(self):
        binning = Round()
        self.assertEqual(0.5, binning(0.5))
        self.assertEqual(0.5, binning(1.4))
        self.assertEqual(104.5, binning(104.5))
        self.assertEqual(-0.5, binning(-0.4))
        self.assertEqual(-0.5, binning(-0.5))
        self.assertEqual(-1.5, binning(-1.4))
        self.assertEqual(-1.5, binning(-1.5))
        self.assertEqual(-2.5, binning(-1.6))

    def test_call_width_2(self):
        binning = Round(2)
        self.assertEqual( -3, binning( -2.9))
        self.assertEqual( -3, binning( -2  ))
        self.assertEqual( -3, binning( -1.1))
        self.assertEqual( -1, binning( -0.9))
        self.assertEqual( -1, binning(  0  ))
        self.assertEqual( -1, binning(  0.9))
        self.assertEqual(  1, binning(  1.1))
        self.assertEqual(  1, binning(  2  ))
        self.assertEqual(  1, binning(  2.9))

    def test_call_width_2_aboundary_0(self):
        binning = Round(2, 0)
        self.assertEqual( -2, binning( -1.9))
        self.assertEqual( -2, binning( -1  ))
        self.assertEqual( -2, binning( -0.1))
        self.assertEqual(  0, binning(  0.1))
        self.assertEqual(  0, binning(  1  ))
        self.assertEqual(  0, binning(  1.9))
        self.assertEqual(  2, binning(  2.1))
        self.assertEqual(  2, binning(  3  ))
        self.assertEqual(  2, binning(  3.9))

    def test_call_decimal_width(self):
        binning = Round(0.02, 0.005)
        self.assertAlmostEqual(  0.005, binning(  0.005))
        self.assertAlmostEqual(  0.025, binning(  0.025))
        self.assertAlmostEqual(  0.065, binning(  0.081))
        self.assertAlmostEqual( -0.055, binning( -0.048))
        self.assertAlmostEqual( -0.015, binning( -0.015))

    def test_center(self):
        binning = Round(retvalue = 'center')
        self.assertEqual(   1.0, binning(   0.51))
        self.assertEqual(   1.0, binning(   1.41))
        self.assertEqual( 105.0, binning( 104.6 ))
        self.assertEqual(  -0.0, binning(  -0.4 ))
        self.assertEqual(  -1.0, binning( -0.51 ))
        self.assertEqual(  -1.0, binning( -1.4  ))
        self.assertEqual(  -1.0, binning( -1.5  ))

        binning = Round(0.02, 0.005, retvalue = 'center')
        self.assertAlmostEqual(  0.015, binning(  0.005))
        self.assertAlmostEqual(  0.035, binning(  0.025))
        self.assertAlmostEqual(  0.075, binning(  0.081))
        self.assertAlmostEqual( -0.045, binning( -0.048))
        self.assertAlmostEqual( -0.005, binning( -0.015))

    def test_onBoundary(self):
        binning = Round()
        self.assertEqual( -1.5, binning( -1.5))
        self.assertEqual( -0.5, binning( -0.5))
        self.assertEqual(  0.5, binning(  0.5))
        self.assertEqual(  1.5, binning(  1.5))

        binning = Round(retvalue = 'center')
        self.assertEqual( -1, binning( -1.5))
        self.assertEqual(  0, binning( -0.5))
        self.assertEqual(  1, binning(  0.5))
        self.assertEqual(  2, binning(  1.5))

        binning = Round(0.02, 0.005)
        self.assertEqual( -0.035, binning( -0.035))
        self.assertEqual( -0.015, binning( -0.015))
        self.assertEqual(  0.005, binning(  0.005))
        self.assertEqual(  0.025, binning(  0.025))
        self.assertEqual(  0.045, binning(  0.045))

        binning = Round(0.02, 0.005, retvalue = 'center')
        self.assertAlmostEqual( -0.025, binning( -0.035))
        self.assertAlmostEqual( -0.005, binning( -0.015))
        self.assertAlmostEqual(  0.015, binning(  0.005))
        self.assertAlmostEqual(  0.035, binning(  0.025))
        self.assertAlmostEqual(  0.055, binning(  0.045))

    def test_next(self):
        binning = Round()
        self.assertEqual( -0.5, binning.next( -1.5))
        self.assertEqual(  0.5, binning.next( -0.5))
        self.assertEqual(  1.5, binning.next(  0.5))
        self.assertEqual(  2.5, binning.next(  1.5))

        binning = Round(retvalue = 'center')
        self.assertEqual( 0, binning.next( -1))
        self.assertEqual( 1, binning.next(  0))
        self.assertEqual( 2, binning.next(  1))
        self.assertEqual( 3, binning.next(  2))

        binning = Round(0.02, 0.005)
        self.assertEqual( -0.015, binning.next( -0.035))
        self.assertEqual(  0.005, binning.next( -0.015))
        self.assertEqual(  0.025, binning.next(  0.005))
        self.assertEqual(  0.045, binning.next(  0.025))
        self.assertEqual(  0.065, binning.next(  0.045))

        binning = Round(0.02, 0.005, retvalue = 'center')
        self.assertAlmostEqual( -0.005, binning.next( -0.025))
        self.assertAlmostEqual(  0.015, binning.next( -0.005))
        self.assertAlmostEqual(  0.035, binning.next(  0.015))
        self.assertAlmostEqual(  0.055, binning.next(  0.035))
        self.assertAlmostEqual(  0.075, binning.next(  0.055))

    def test_valid(self):
        binning = Round(valid = lambda x: x >= 0)
        self.assertEqual(  0.5, binning(  1))
        self.assertEqual( -0.5, binning(  0))
        self.assertEqual( None, binning( -1))

##__________________________________________________________________||
