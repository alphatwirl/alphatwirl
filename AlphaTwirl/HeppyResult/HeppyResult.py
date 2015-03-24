# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
import os

from Component import Component

##____________________________________________________________________________||
defaultExcludeList = ('Chunks', 'failed')

##____________________________________________________________________________||
class HeppyResult(object):
    def __init__(self, path, componentNames = None, excludeList = defaultExcludeList):
        self.path = path
        allComponentNames = [n for n in os.listdir(path) if os.path.isdir(os.path.join(path, n)) and n not in excludeList]
        if componentNames is not None:
            nonexistentComponent =  [c for c in componentNames if c not in allComponentNames]
            if len(nonexistentComponent) > 0:
                raise ValueError("No such components: " + ", ".join(nonexistentComponent))
            self.componentNames = componentNames
        else:
            self.componentNames = allComponentNames

        self._compDict = { }

    def __getattr__(self, name):
        if name not in self._compDict:
            if name not in self.componentNames:
                raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
            path = os.path.join(self.path, name)
            self._compDict[name] = Component(path)
        return self._compDict[name]

    def components(self):
        return [getattr(self, n) for n in self.componentNames]

##____________________________________________________________________________||
