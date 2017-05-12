# Tai Sakuma <tai.sakuma@cern.ch>
from alphatwirl.selection.factories.LambdaStrFactory import LambdaStrFactory
import unittest

##__________________________________________________________________||
class MockLambdaStr(object):
    def __init__(self, lambda_str, name = None):
        self.name = name
        self.lambda_str = lambda_str

##__________________________________________________________________||
class Test_LambdaStrFactory(unittest.TestCase):

    def test_standard(self):
        obj = LambdaStrFactory(
            lambda_str = 'ev : ev.var1[0] >= 10',
            name = 'var1',
            LambdaStrClass = MockLambdaStr
        )
        self.assertIsInstance(obj, MockLambdaStr)
        self.assertEqual('ev : ev.var1[0] >= 10', obj.lambda_str)
        self.assertEqual('var1', obj.name)

    def test_no_name(self):
        obj = LambdaStrFactory(
            lambda_str = 'ev : ev.var1[0] >= 10',
            LambdaStrClass = MockLambdaStr
        )
        self.assertIsInstance(obj, MockLambdaStr)
        self.assertEqual('ev : ev.var1[0] >= 10', obj.lambda_str)
        self.assertEqual(None, obj.name)

    def test_format(self):
        obj = LambdaStrFactory(
            lambda_str = 'ev : {low} <= ev.var1[0] = {high}',
            name = 'var1',
            low = 100,
            high = 200,
            LambdaStrClass = MockLambdaStr
        )
        self.assertIsInstance(obj, MockLambdaStr)
        self.assertEqual('ev : 100 <= ev.var1[0] = 200', obj.lambda_str)
        self.assertEqual('var1', obj.name)

##__________________________________________________________________||
