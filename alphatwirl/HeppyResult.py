# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
import os
import ast

##____________________________________________________________________________||
class HeppyResult(object):
    def __init__(self, path):
        self.path = path
        excludeList = ('Chunks', 'failed')
        self.componentNames = [n for n in os.listdir(path) if os.path.isdir(os.path.join(path, n)) and n not in excludeList]

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
class Component(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.analyzerNames = [n for n in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, n))]

        self._anaDict = { }
        self._cfg = None
        self._readConfig = ReadComponentConfig()

    def __getattr__(self, name):
        if name not in self._anaDict:
            if name not in self.analyzerNames:
                raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
            path = os.path.join(self.path, name)
            self._anaDict[name] = Analyzer(path)
        return self._anaDict[name]

    def analyzers(self):
        return [getattr(self, n) for n in self.analyzerNames]

    def config(self):
        if self._cfg is None:
            path = os.path.join(self.path, 'config.txt')
            self._cfg = self._readConfig(path)
        return self._cfg

##____________________________________________________________________________||
class ReadComponentConfig(object):
    def __call__(self, path):
        file = open(path)
        return self._readImp(file)

    def _readImp(self, file):
        file.readline() # skip the 1st line
        l = [[e.strip() for e in l.split(":", 1)] for l in file]
        return dict([(e[0], self._literal_eval_or_string(e[1])) for e in l])

    def _literal_eval_or_string(self, val):
        try:
            return ast.literal_eval(val)
        except:
            return val

##____________________________________________________________________________||
class Analyzer(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

##____________________________________________________________________________||
if __name__ == '__main__':
    pass
