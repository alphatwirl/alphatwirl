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
        expected = [1.9952623149688795, 19.952623149688797, 199.52623149688787]
        actual = binning((2, 20, 200))
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)

    def test_call_center(self):
        binning = RoundLog(retvalue = 'center')
        expected = [2.2387211385683394, 22.3872113856834, 223.872113856834]
        actual = binning((2, 20, 200))
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)

    def test_next(self):
        binning = RoundLog(retvalue = 'center')
        expected = [2.8183829312644537, 28.183829312644534, 281.8382931264455]
        actual = binning.next([2.2387211385683394, 22.3872113856834, 223.872113856834])
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)

    def test_call_zero(self):
        binning = RoundLog()
        self.assertIsNone(binning(0))

    def test_call_negative(self):
        binning = RoundLog()
        self.assertIsNone(binning(-1))

    def test_valid(self):
        binning = RoundLog(valid = lambda x: x >= 10)
        expected = [12.589254117941675, 10.0, None]
        actual = binning((13, 10, 7))
        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a)

##____________________________________________________________________________||
