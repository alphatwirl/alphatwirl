from ...EventSelectionFactories.AnyFactory import AnyFactory
from ...EventSelectionModules.EventSelectionAll import EventSelectionAll
from ...EventSelectionModules.EventSelectionAny import EventSelectionAny
from ...EventSelectionModules.LambdaStr import LambdaStr
from ...event_selection_str import event_selection_str
import unittest

##__________________________________________________________________||
class Test_AnyFactory(unittest.TestCase):

    def test_obj(self):
        path_cfg_list = ("ev : ev.nJet[0] >= 2", "ev : ev.nMET[0] >= 200")
        kargs = dict(arg1 = 10, arg2 = 20, AnyClass = EventSelectionAny, LambdaStrClass = LambdaStr)
        obj = AnyFactory(path_cfg_list, name = 'test_any', **kargs)

##__________________________________________________________________||
