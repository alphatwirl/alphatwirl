import AlphaTwirl.Summary as Summary
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class TestWeightCalculatorOne(unittest.TestCase):

    def test_events(self):
        weight = Summary.WeightCalculatorOne()
        self.assertEqual(1.0, weight(MockEvent()))

##__________________________________________________________________||
