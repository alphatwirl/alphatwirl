# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
import os

##____________________________________________________________________________||
class Heppy(object):
    def __init__(self, path):
        self.path = path
        excludeList = ('Chunks', 'failed')
        self.componentNames = [n for n in os.listdir(path) if os.path.isdir(os.path.join(path, n)) and n not in excludeList]

        self._compDict = { }

    def __getattr__(self, name):
        if name not in self._compDict:
            if name not in self.componentNames:
                raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
            compPath = os.path.join(self.path, name)
            self._compDict[name] = Component(compPath)
        return self._compDict[name]

    def components(self):
        return [getattr(self, n) for n in self.componentNames]

##____________________________________________________________________________||
class Component(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.analyzerNames = [n for n in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, n))]

    def __getattr__(self, name):
        if name not in self.analyzerNames:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
        return Analyzer(self.path, name)

##____________________________________________________________________________||
class Analyzer(object):
    def __init__(self, path, name):
        self.path = os.path.join(path, name)

##____________________________________________________________________________||
if __name__ == '__main__':
    pass
