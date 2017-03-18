import alphatwirl.summary as summary
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class TestWeightCalculatorOne(unittest.TestCase):

    def test_events(self):
        weight = summary.WeightCalculatorOne()
        self.assertEqual(1.0, weight(MockEvent()))

##__________________________________________________________________||
