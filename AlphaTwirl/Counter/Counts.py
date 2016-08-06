# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import collections

##__________________________________________________________________||
class Counts(object):
    def __init__(self):
        self._counts = { }
        self._val_names = ('n', 'nvar') # (count, variance)

    def count(self, key, val = None, weight = 1):
        self.addKey(key)
        self._counts[key][self._val_names[0]] += weight
        self._counts[key][self._val_names[1]] += weight**2

    def addKey(self, key):
        if key not in self._counts:
            self._counts[key] = collections.OrderedDict(
                ((self._val_names[0], 0.0), (self._val_names[1], 0.0))
            )

    def keys(self):
        return self._counts.keys()

    def valNames(self):
        return self._val_names

    def copyFrom(self, src):
        self._counts.clear()
        self._counts.update(src._counts)

    def results(self):
        return self._counts

##__________________________________________________________________||
