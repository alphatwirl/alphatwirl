from alphatwirl.selection.factories.FactoryDispatcher import FactoryDispatcher
from alphatwirl.selection.factories.FactoryDispatcher import expand_path_cfg
from alphatwirl.selection.modules.LambdaStr import LambdaStr
import unittest
import os, sys

##__________________________________________________________________||
# @unittest.skip("skipping")
class Test_FactoryDispatcher(unittest.TestCase):

    def setUp(self):

        self.aliasDict = {
            'alias1': 'ev : ev.var1[0] >= 10',
            'alias2': ('ev : ev.var2[0] >= 20', dict(name = 'name2')),
            'alias3': 'alias1',
            'alias4': 'alias3',
            'alias5': 'ev : ev.var4[0] == {n}',
            'alias6': ('ev : {low} <= ev.var5[0] < {high}', dict(low = 11, high = 20))
        }

        ## update sys.path (this can be removed when the problem of module path is resolved)
        self.twoUpDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        if not self.twoUpDir in sys.path:
            self.twoUpDirAdded = True
            sys.path.append(self.twoUpDir)
        else:
            self.twoUpDirAdded = False

    def tearDown(self):

        ## put sys.path back (this can be removed when the problem of module path is resolved)
        if self.twoUpDirAdded:
            sys.path.remove(self.twoUpDir)

    def test_string(self):
        kargs = dict(arg1 = 10, arg2 = 20,
                     aliasDict = self.aliasDict,
                     LambdaStrClass = LambdaStr)
        path_cfg = 'alias1'
        obj = FactoryDispatcher(path_cfg = path_cfg, **kargs)
        self.assertIsInstance(obj, LambdaStr)
        self.assertEqual('alias1', obj.name)
        self.assertEqual('ev : ev.var1[0] >= 10', obj.lambda_str)

##__________________________________________________________________||
class Test_expand_path_cfg(unittest.TestCase):

    def setUp(self):
        self.aliasDict = {
            'alias1': 'ev : ev.var1[0] >= 10',
            'alias2': ('ev : ev.var2[0] >= 20', dict(name = 'name2')),
            'alias3': 'alias1',
            'alias4': 'alias3',
            'alias5': 'ev : ev.var4[0] == {n}',
            'alias6': ('ev : {low} <= ev.var5[0] < {high}', dict(low = 11, high = 20))
        }

    def test_alias1_standard(self):

        path_cfg = 'alias1'

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.var1[0] >= 10',
            name = 'alias1'
        )

        self.assertEqual(expected, actual)

    def test_alias1_with_name(self):

        path_cfg = ('alias1', dict(name = 'name1'))

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.var1[0] >= 10',
            name = 'name1'
        )

        self.assertEqual(expected, actual)

    def test_alias2_name_has_priority_over_alias(self):

        path_cfg = 'alias2'

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.var2[0] >= 20',
            name = 'name2' #  name has priority over alias
        )

        self.assertEqual(expected, actual)

    def test_alias2_name_can_be_overridden(self):

        path_cfg = ('alias2', dict(name = 'new_name2'))

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.var2[0] >= 20',
            name = 'new_name2' # name can be overridden
        )

        self.assertEqual(expected, actual)

    def test_alias3_alias_of_alias(self):

        path_cfg = 'alias3'

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.var1[0] >= 10',
            name = 'alias3' # the outermost alias has priority
        )

        self.assertEqual(expected, actual)

    def test_alias4_alias_of_alias_of_alias(self):

        path_cfg = 'alias4'

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.var1[0] >= 10',
            name = 'alias4' # the outermost alias has priority
        )

        self.assertEqual(expected, actual)

    def test_alias5_not_formatted(self):

        path_cfg = ('alias5', dict(n = 30))

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.var4[0] == {n}', # not formatted
            n = 30,
            name = 'alias5'
        )

        self.assertEqual(expected, actual)

    def test_alias6_not_formatted_with_default_values(self):

        path_cfg = 'alias6'

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : {low} <= ev.var5[0] < {high}',
            low = 11,
            high = 20,
            name = 'alias6',
        )

        self.assertEqual(expected, actual)

    def test_alias6_not_formatted_with_default_values_overridden(self):

        path_cfg = ('alias6', dict(high = 30))

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : {low} <= ev.var5[0] < {high}',
            low = 11,
            high = 30,
            name = 'alias6'
        )

        self.assertEqual(expected, actual)

    def test_string_lambda_str(self):

        path_cfg = 'ev : ev.nJets[0] >= 2'

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.nJets[0] >= 2',
        )

        self.assertEqual(expected, actual)

    def test_string_lambda_str_not_formatted(self):

        path_cfg = 'ev : ev.nJets[0] >= {n}'

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'LambdaStrFactory',
            lambda_str = 'ev : ev.nJets[0] >= {n}',
        )

        self.assertEqual(expected, actual)

    def test_dict_raise_multiple_All_Any_Not(self):

        expand_path_cfg(path_cfg = dict(All = ()))
        expand_path_cfg(path_cfg = dict(Any = ()))
        expand_path_cfg(path_cfg = dict(Not = ()))

        path_cfg = dict(All = (), Any = ())
        self.assertRaises(ValueError, expand_path_cfg, path_cfg = path_cfg)

        path_cfg = dict(All = (), Not = ())
        self.assertRaises(ValueError, expand_path_cfg, path_cfg = path_cfg)

        path_cfg = dict(Any = (), Not = ())
        self.assertRaises(ValueError, expand_path_cfg, path_cfg = path_cfg)

    def test_dict_raise_no_All_Any_Not(self):
        path_cfg = dict()
        self.assertRaises(ValueError, expand_path_cfg, path_cfg = path_cfg)

    def test_dict_All(self):

        path_cfg = dict(All = (dict(factory = 'factory1'), dict(factory = 'factory2')), name = 'test_all', arg2 = 2, arg3 = 3)

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'AllFactory',
            path_cfg_list = (dict(factory = 'factory1'), dict(factory = 'factory2')),
            name = 'test_all',
            arg2 = 2, arg3 = 3
        )

        self.assertEqual(expected, actual)

    def test_dict_Any(self):

        path_cfg = dict(Any = (dict(factory = 'factory1'), dict(factory = 'factory2')), name = 'test_any', arg2 = 2, arg3 = 3)

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'AnyFactory',
            path_cfg_list = (dict(factory = 'factory1'), dict(factory = 'factory2')),
            name = 'test_any',
            arg2 = 2, arg3 = 3
        )

        self.assertEqual(expected, actual)

    def test_dict_Not(self):

        path_cfg = dict(Not = dict(factory = 'factory1'), name = 'test_not', arg2 = 2, arg3 = 3)

        actual = expand_path_cfg(path_cfg = path_cfg, aliasDict = self.aliasDict)

        expected = dict(
            factory = 'NotFactory',
            path_cfg = dict(factory = 'factory1'),
            name = 'test_not',
            arg2 = 2, arg3 = 3
        )

        self.assertEqual(expected, actual)

##__________________________________________________________________||
