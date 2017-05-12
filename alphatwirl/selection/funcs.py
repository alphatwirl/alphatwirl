# Tai Sakuma <tai.sakuma@cern.ch>
from .EventSelectionModules.basic import All
from .EventSelectionModules.basic import EventSelectionAny
from .EventSelectionModules.basic import EventSelectionNot
from .EventSelectionModules.LambdaStr import LambdaStr
from .EventSelectionFactories.FactoryDispatcher import FactoryDispatcher

import os, sys

##__________________________________________________________________||
thisDir = os.path.dirname(os.path.realpath(__file__))
if not thisDir in sys.path: sys.path.append(thisDir)

##__________________________________________________________________||
def build_selection(**kargs):

    if 'aliasDict' not in kargs: kargs['aliasDict'] = { }

    if 'AllClass' not in kargs: kargs['AllClass'] = All
    if 'AnyClass' not in kargs: kargs['AnyClass'] = EventSelectionAny
    if 'NotClass' not in kargs: kargs['NotClass'] = EventSelectionNot
    if 'LambdaStrClass' not in kargs: kargs['LambdaStrClass'] = LambdaStr

    return FactoryDispatcher(**kargs)

##__________________________________________________________________||
