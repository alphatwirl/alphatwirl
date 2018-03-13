# Tai Sakuma <tai.sakuma@gmail.com>
from .modules.basic import All
from .modules.basic import Any
from .modules.basic import Not
from .modules.LambdaStr import LambdaStr
from .factories.factory import FactoryDispatcher

import os, sys

##__________________________________________________________________||
thisDir = os.path.dirname(os.path.realpath(__file__))
if not thisDir in sys.path: sys.path.append(thisDir)

##__________________________________________________________________||
def build_selection(**kargs):

    if 'aliasDict' not in kargs: kargs['aliasDict'] = { }

    if 'AllClass' not in kargs: kargs['AllClass'] = All
    if 'AnyClass' not in kargs: kargs['AnyClass'] = Any
    if 'NotClass' not in kargs: kargs['NotClass'] = Not
    if 'LambdaStrClass' not in kargs: kargs['LambdaStrClass'] = LambdaStr

    return FactoryDispatcher(**kargs)

##__________________________________________________________________||
