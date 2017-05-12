import unittest

from .. import buildEventSelection
from ..EventSelectionModules.EventSelectionAll import EventSelectionAll
from ..EventSelectionModules.EventSelectionAny import EventSelectionAny
from ..EventSelectionModules.EventSelectionNot import EventSelectionNot
from ..EventSelectionModules.LambdaStr import LambdaStr

##__________________________________________________________________||
class MockFactoryDispatcher(object):
    def __call__(self, **kargs):
        return kargs

##__________________________________________________________________||
class Test_buildEventSelection(unittest.TestCase):

    def setUp(self):
        self._org_FactoryDispatcher = buildEventSelection.FactoryDispatcher
        buildEventSelection.FactoryDispatcher = MockFactoryDispatcher()

    def tearDown(self):
        buildEventSelection.FactoryDispatcher = self._org_FactoryDispatcher

    def test_call_kargs(self):

        kargs = dict(
            arg1 = 10,
            arg2 = 20,
            level = dict(factory = 'test_level1', arg2 = 2, arg3 = 3)
        )

        obj = buildEventSelection.buildEventSelection(**kargs)

        self.assertIsNot(kargs, obj)
        obj.pop('AllClass')
        obj.pop('AnyClass')
        obj.pop('NotClass')
        obj.pop('LambdaStrClass')
        obj.pop('aliasDict')
        self.assertEqual(kargs, obj)

    def test_call_default_modules(self):

        obj = buildEventSelection.buildEventSelection(
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
