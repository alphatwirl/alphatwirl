# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import os

##__________________________________________________________________||
class Analyzer(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

##__________________________________________________________________||
