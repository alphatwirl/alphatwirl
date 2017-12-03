# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.selection.modules.LambdaStr import LambdaStr
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class Test_LambdaStr(unittest.TestCase):

    def test_standard(self):
        obj = LambdaStr(lambda_str = 'ev : True', name = 'test_true')

        event = MockEvent()
        obj.begin(event)
        self.assertTrue(callable(obj.func))

        event = MockEvent()
        self.assertTrue(obj(event))

        event = MockEvent()
        self.assertTrue(obj.event(event))

        obj.end()
        self.assertIsNone(obj.func)


    def test_raise(self):
        obj = LambdaStr(lambda_str = 'ev: aaa', name = 'test_true')

        event = MockEvent()
        obj.begin(event)

        event = MockEvent()
        self.assertRaises(ValueError, obj, event)

        obj.end()


##__________________________________________________________________||
