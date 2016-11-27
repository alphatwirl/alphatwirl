# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import numpy as np

##__________________________________________________________________||
class CountImp(object):
    """
    Args:
        val : an empty tuple for a count. None not to be counted
        weight (float) : The weight
    """

    def __init__(self, val = None, weight = 1):

        if val is None:
            self.summary = np.array((0, 0))
            return

        self.summary = np.array((weight, weight**2))

    def copy(self):
        ret = self.__class__()
        ret.summary = self.summary.copy()
        return ret

    def __add__(self, other):
        ret = self.copy()
        ret.summary = ret.summary + other.summary
        return ret

##__________________________________________________________________||
class Count(object):
    def __init__(self):
        self._results = { }

    def add(self, key, val = None, weight = 1):
        self.add_key(key)
        self._results[key] = self._results[key] + CountImp(val, weight)

    def add_key(self, key):
        if key not in self._results:
            self._results[key] = CountImp()

    def keys(self):
        return self._results.keys()

    def copy_from(self, src):
        self._results.clear()
        self._results.update(src._results)

    def results(self):
        ## return self._results
        return {k: v.summary for k, v in self._results.iteritems()}

    def __add__(self, other):
        ret = Count()
        results = {k: v.copy() for k, v in self._results.iteritems()}
        if not other == 0: # other is 0 when e.g. sum([obj1, obj2])
            self._add_results_inplace(results, other._results)
        ret._results.clear()
        ret._results.update(results)
        return ret

    def __iadd__(self, other):
        self._add_results_inplace(self._results, other._results)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def _add_results_inplace(self, res1, res2):
        # res1 += res2, modify res1
        for k, v in res2.iteritems():
            if k not in self._results:
                res1[k] = v.copy()
            else:
                res1[k] = self._results[k] + v

##__________________________________________________________________||
