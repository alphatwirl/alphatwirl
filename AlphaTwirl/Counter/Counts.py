# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import collections

##__________________________________________________________________||
class Counts(object):
    def __init__(self):
        self._counts = { }

    def count(self, key, w = 1):
        self.addKey(key)
        self._counts[key]['n'] += w
        self._counts[key]['nvar'] += w**2

    def addKey(self, key):
        if key not in self._counts:
            self._counts[key] = collections.OrderedDict((('n', 0.0), ('nvar', 0.0)))

    def keys(self):
        return self._counts.keys()

    def valNames(self):
        return ('n', 'nvar')

    def copyFrom(self, src):
        self._counts.clear()
        self._counts.update(src._counts)

    def results(self):
        return self._counts

##__________________________________________________________________||
