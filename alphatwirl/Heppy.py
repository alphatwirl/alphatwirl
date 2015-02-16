# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
import os

##____________________________________________________________________________||
class Components(object):
    def __init__(self, path):
        self.path = path
        excludeList = ('Chunks', 'failed')
        self.names = [n for n in os.listdir(path) if os.path.isdir(path + '/' + n) and n not in excludeList]

    def __getitem__(self, i):
        return Component(self.path, self.names[i])

##____________________________________________________________________________||
class Component(object):
    def __init__(self, path, name):
        self.path = path + '/' + name
        self.name = name
        self.analyzerNames = [n for n in os.listdir(self.path) if os.path.isdir(self.path + '/' + n)]

    def __getattr__(self, name):
        if name not in self.analyzerNames:
            raise AttributeError("no attribute '" + name + "'")
        return Analyzer(self.path, name)

##____________________________________________________________________________||
class Analyzer(object):
    def __init__(self, path, name):
        self.path = path + '/' + name

##____________________________________________________________________________||
if __name__ == '__main__':
    pass
