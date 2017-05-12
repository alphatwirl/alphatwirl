from alphatwirl.selection.factories.LambdaStrFromDictFactory import LambdaStrFromDictFactory
from alphatwirl.selection.modules.LambdaStr import LambdaStr
import unittest

##__________________________________________________________________||
class Test_LambdaStrFromDictFactory(unittest.TestCase):

    def setUp(self):
        self.aliasDict = {
            'JSON': "ev : ev.inCertifiedLumiSections[0]",
            'nMuonsIsolated': 'ev : ev.nMuonsIsolated[0] == {n}'
        }


    def test_obj(self):
        obj = LambdaStrFromDictFactory(key = 'JSON',
                                       LambdaStrClass = LambdaStr,
                                       aliasDict = self.aliasDict
                                       )

        self.assertIsInstance(obj, LambdaStr)
        self.assertEqual('ev : ev.inCertifiedLumiSections[0]', obj.lambda_str)
        self.assertEqual('JSON', obj.name)

    def test_obj_format(self):
        obj = LambdaStrFromDictFactory(key = 'nMuonsIsolated',
                                       n = 1,
                                       LambdaStrClass = LambdaStr,
                                       aliasDict = self.aliasDict
                                       )

        self.assertIsInstance(obj, LambdaStr)
        self.assertEqual('ev : ev.nMuonsIsolated[0] == 1', obj.lambda_str)
        self.assertEqual('nMuonsIsolated', obj.name)

##__________________________________________________________________||
