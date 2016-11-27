# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import numpy as np
import copy

##__________________________________________________________________||
class SumImp(object):

    def __init__(self, val = None, weight = 1, contents = None):

        if contents is not None:
            self.contents = np.array(contents)
            return

        self.contents = np.array(val*weight)

    def __add__(self, other):
        contents = self.contents + other.contents
        return self.__class__(contents = contents)

##__________________________________________________________________||
class Sum(object):
    def __init__(self, initial_val = (0, )):
        self._results = { }
        self.Summary = SumImp
        self.initial_contents = initial_val

    def add(self, key, val, weight = 1):
        self.add_key(key)
        self._results[key] = self._results[key] + self.Summary(val, weight)

    def add_key(self, key):
        if key not in self._results:
            self._results[key] = self.Summary(contents = self.initial_contents)

    def keys(self):
        return self._results.keys()

    def copy_from(self, src):
        self._results.clear()
        self._results.update(src._results)

    def results(self):
        ## return self._results
        return {k: v.contents for k, v in self._results.iteritems()}

    def __add__(self, other):
        ret = self.__class__()
        results = {k: copy.deepcopy(v) for k, v in self._results.iteritems()}
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
                res1[k] = copy.deepcopy(v)
            else:
                res1[k] = self._results[k] + v

##__________________________________________________________________||
