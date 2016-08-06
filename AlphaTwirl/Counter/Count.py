# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import numpy as np

##__________________________________________________________________||
class Count(object):
    def __init__(self):
        self._results = { }

    def count(self, key, val = None, weight = 1):
        self.addKey(key)
        self._results[key] = self._results[key] + np.array((weight, weight**2)) # (n, nvar)

    def addKey(self, key):
        if key not in self._results:
            self._results[key] = np.array((0, 0)) # (n, nvar)

    def keys(self):
        return self._results.keys()

    def copyFrom(self, src):
        self._results.clear()
        self._results.update(src._results)

    def results(self):
        return self._results

##__________________________________________________________________||
