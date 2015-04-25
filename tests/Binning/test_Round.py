from AlphaTwirl.Binning import Round
import unittest

##____________________________________________________________________________||
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

    def test_call_with_list(self):
        binning = Round()
        self.assertEqual([0.5, 0.5, 104.5, -0.5, -0.5, -1.5, -1.5], binning((0.5, 1.4, 104.5, -0.4, -0.5, -1.4, -1.5 )))

    def test_call_width_2(self):
        binning = Round(2)
        self.assertEqual([-3, -3, -3, -1, -1, -1, 1, 1, 1], binning((-2.9, -2, -1.1, -0.9, 0, 0.9, 1.1, 2, 2.9)))

    def test_call_width_2_aboundary_0(self):
        binning = Round(2, 0)
        self.assertEqual([-2, -2, -2, 0, 0, 0, 2, 2, 2], binning((-1.9, -1, -0.1, 0.1, 1, 1.9, 2.1, 3, 3.9)))

    def test_call_decimal_width(self):
        binning = Round(0.02, 0.005)
        expected = [0.005, 0.025, 0.065, -0.055, -0.015]
        actual = binning((0.005, 0.025, 0.081, -0.048, -0.015))
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)

    def test_center(self):
        binning = Round(retvalue = 'center')
        self.assertEqual([1.0, 1.0, 105.0, -0.0, -1.0, -1.0, -1.0], binning((0.51, 1.41, 104.6, -0.4, -0.51, -1.4, -1.5 )))

        binning = Round(0.02, 0.005, retvalue = 'center')
        expected = [0.015, 0.035, 0.075, -0.045, -0.005]
        actual = binning((0.005, 0.025, 0.081, -0.048, -0.015))
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)

    def test_onBoundary(self):
        binning = Round()
        self.assertEqual([-1.5, -0.5, 0.5, 1.5], binning((-1.5, -0.5, 0.5, 1.5)))

        binning = Round(retvalue = 'center')
        self.assertEqual([-1, 0, 1, 2], binning((-1.5, -0.5, 0.5, 1.5)))

        binning = Round(0.02, 0.005)
        self.assertEqual([-0.035, -0.015, 0.005, 0.025, 0.045], binning((-0.035, -0.015, 0.005, 0.025, 0.045)))

        binning = Round(0.02, 0.005, retvalue = 'center')
        expected = [-0.025, -0.005, 0.015, 0.035, 0.055]
        actual = binning((-0.035, -0.015, 0.005, 0.025, 0.045))
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)

    def test_next(self):
        binning = Round()
        self.assertEqual([-0.5, 0.5, 1.5, 2.5], binning.next([-1.5, -0.5, 0.5, 1.5]))

        binning = Round(retvalue = 'center')
        self.assertEqual([0, 1, 2, 3], binning.next([-1, 0, 1, 2]))

        binning = Round(0.02, 0.005)
        self.assertEqual([-0.015, 0.005, 0.025, 0.045, 0.065], binning.next([-0.035, -0.015, 0.005, 0.025, 0.045]))

        binning = Round(0.02, 0.005, retvalue = 'center')
        expected = [-0.005, 0.015, 0.035, 0.055, 0.075]
        actual = binning.next([-0.025, -0.005, 0.015, 0.035, 0.055])
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)


    def test_valid(self):
        binning = Round(valid = lambda x: x >= 0)
        self.assertEqual([0.5, -0.5, None], binning((1, 0, -1)))

##____________________________________________________________________________||
