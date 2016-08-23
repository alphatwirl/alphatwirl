# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import numpy as np

##__________________________________________________________________||
class Scan(object):
    def __init__(self, n = None):
        self._results = [ ]
        self.n = n
        self.i = 0

    def add(self, key, val, weight = 1):
        if self.n is not None and self.n <= self.i: return
        self._results.append(key + val)
        self.i += 1

    def add_key(self, key):
        pass

    def keys(self):
        return [ ]

    def copy_from(self, src):
        self._results[:] = src._results

    def results(self):
        return self._results

    def __add__(self, other):
        ret = Scan()
        results = list(self._results) # copy
        if not other == 0: # other is 0 when e.g. sum([obj1, obj2])
            self._add_results_inplace(results, other._results)
        ret._results[:] = results
        return ret

    def __iadd__(self, other):
        self._add_results_inplace(self._results, other._results)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def _add_results_inplace(self, res1, res2):
        res1.extend(res2)

##__________________________________________________________________||
