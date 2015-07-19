import AlphaTwirl.Counter as Counter
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class TestWeightCalculatorOne(unittest.TestCase):

    def test_events(self):
        weight = Counter.WeightCalculatorOne()
        self.assertEqual(1.0, weight(MockEvent))

##__________________________________________________________________||
