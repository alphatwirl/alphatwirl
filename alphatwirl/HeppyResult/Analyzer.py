# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os

##__________________________________________________________________||
class Analyzer(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

##__________________________________________________________________||
