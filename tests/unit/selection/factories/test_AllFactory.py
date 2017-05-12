from alphatwirl.selection.factories.AllFactory import AllFactory
from alphatwirl.selection.modules.basic import All
from alphatwirl.selection.modules.basic import Any
from alphatwirl.selection.modules.LambdaStr import LambdaStr
import unittest

##__________________________________________________________________||
class Test_AllFactory(unittest.TestCase):

    def test_obj(self):
        path_cfg_list = ("ev : ev.nJet[0] >= 2", "ev : ev.nMET[0] >= 200")
        kargs = dict(arg1 = 10, arg2 = 20, AllClass = All, LambdaStrClass = LambdaStr)
        obj = AllFactory(path_cfg_list, name = 'test_all', **kargs)

##__________________________________________________________________||
