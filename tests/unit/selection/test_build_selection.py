import sys
import unittest

from alphatwirl.selection import build_selection
from alphatwirl.selection.modules import All
from alphatwirl.selection.modules import Any
from alphatwirl.selection.modules import Not
from alphatwirl.selection.modules.LambdaStr import LambdaStr

##__________________________________________________________________||
class MockFactoryDispatcher(object):
    def __call__(self, **kargs):
        return kargs

##__________________________________________________________________||
class Test_buildSelection(unittest.TestCase):

    def setUp(self):
        self.module = sys.modules['alphatwirl.selection.funcs']
        self._org_FactoryDispatcher = self.module.FactoryDispatcher
        self.module.FactoryDispatcher = MockFactoryDispatcher()

    def tearDown(self):
        self.module.FactoryDispatcher = self._org_FactoryDispatcher

    def test_call_kargs(self):

        kargs = dict(
            arg1 = 10,
            arg2 = 20,
            level = dict(factory = 'test_level1', arg2 = 2, arg3 = 3)
        )

        obj = build_selection(**kargs)

        self.assertIsNot(kargs, obj)
        obj.pop('AllClass')
        obj.pop('AnyClass')
        obj.pop('NotClass')
        obj.pop('LambdaStrClass')
        obj.pop('aliasDict')
        self.assertEqual(kargs, obj)

    def test_call_default_modules(self):

        obj = build_selection(
            arg1 = 10,
            arg2 = 20,
            level = dict(factory = 'test_level1', arg2 = 2, arg3 = 3)
            )

        self.assertIs(All, obj.pop('AllClass'))
        self.assertIs(Any, obj.pop('AnyClass'))
        self.assertIs(Not, obj.pop('NotClass'))
        self.assertIs(LambdaStr, obj.pop('LambdaStrClass'))
        obj.pop('aliasDict')

        expected = dict(
            arg1 = 10,
            arg2 = 20,
            level = dict(factory = 'test_level1', arg2 = 2, arg3 = 3)
        )
        self.assertEqual(expected, obj)

##__________________________________________________________________||
