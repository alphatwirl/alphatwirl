# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import os

from alphatwirl.misc.deprecation import atdeprecated

##__________________________________________________________________||
@atdeprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class Analyzer(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

##__________________________________________________________________||
