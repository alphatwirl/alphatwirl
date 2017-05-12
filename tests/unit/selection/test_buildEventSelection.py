import sys
import unittest

from alphatwirl.selection import buildEventSelection
from alphatwirl.selection.EventSelectionModules.EventSelectionAll import EventSelectionAll
from alphatwirl.selection.EventSelectionModules.EventSelectionAny import EventSelectionAny
from alphatwirl.selection.EventSelectionModules.EventSelectionNot import EventSelectionNot
from alphatwirl.selection.EventSelectionModules.LambdaStr import LambdaStr

##__________________________________________________________________||
class MockFactoryDispatcher(object):
    def __call__(self, **kargs):
        return kargs

##__________________________________________________________________||
class Test_buildEventSelection(unittest.TestCase):

    def setUp(self):
        self.module = sys.modules['alphatwirl.selection.buildEventSelection']
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

        obj = buildEventSelection(**kargs)

        self.assertIsNot(kargs, obj)
        obj.pop('AllClass')
        obj.pop('AnyClass')
        obj.pop('NotClass')
        obj.pop('LambdaStrClass')
        obj.pop('aliasDict')
        self.assertEqual(kargs, obj)

    def test_call_default_modules(self):

        obj = buildEventSelection(
            arg1 = 10,
            arg2 = 20,
            level = dict(factory = 'test_level1', arg2 = 2, arg3 = 3)
            )

        self.assertIs(EventSelectionAll, obj.pop('AllClass'))
        self.assertIs(EventSelectionAny, obj.pop('AnyClass'))
        self.assertIs(EventSelectionNot, obj.pop('NotClass'))
        self.assertIs(LambdaStr, obj.pop('LambdaStrClass'))
        obj.pop('aliasDict')

        expected = dict(
            arg1 = 10,
            arg2 = 20,
            level = dict(factory = 'test_level1', arg2 = 2, arg3 = 3)
        )
        self.assertEqual(expected, obj)

##__________________________________________________________________||
