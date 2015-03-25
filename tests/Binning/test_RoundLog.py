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
        self.assertEqual([1.9952623149688795, 19.952623149688797, 199.52623149688787], binning((2, 20, 200)))

    def test_call_center(self):
        binning = RoundLog(retvalue = 'center')
        self.assertEqual([2.2387211385683394, 22.3872113856834, 223.872113856834], binning((2, 20, 200)))

    def test_next(self):
        binning = RoundLog(retvalue = 'center')
        self.assertEqual([2.8183829312644537, 28.183829312644534, 281.8382931264455], binning.next([2.2387211385683394, 22.3872113856834, 223.872113856834]))

    def test_call_zero(self):
        binning = RoundLog()
        self.assertIsNone(binning(0))

    def test_call_negative(self):
        binning = RoundLog()
        self.assertIsNone(binning(-1))

    def test_valid(self):
        binning = RoundLog(valid = lambda x: x >= 10)
        self.assertEqual([12.589254117941675, 10.0, None], binning((13, 10, 7)))

##____________________________________________________________________________||
