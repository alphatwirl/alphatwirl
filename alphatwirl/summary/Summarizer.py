# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import collections
import copy

##__________________________________________________________________||
class Summarizer(object):
    def __init__(self, Summary):
        self._results = collections.defaultdict(Summary)
        self.Summary = Summary

    def __repr__(self):
        name_value_pairs = (
            ('Summary',  self.Summary),
            ('results', self._results),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def add(self, key, val = None, weight = 1):
        self._results[key] += self.Summary(val, weight)

    def add_key(self, key):
        self._results[key]

    def keys(self):
        return self._results.keys()

    def results(self):
        return self._results

    def __add__(self, other):
        results = copy.deepcopy(self._results) # this copy is very slow
        if not other == 0: # other is 0 when e.g. sum([obj1, obj2])
            self._add_results_inplace(results, other._results)
        ret = self.__class__(self.Summary)
        ret._results = results
        return ret

    def __iadd__(self, other):
        self._add_results_inplace(self._results, other._results)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def _add_results_inplace(self, res1, res2):
        # res1 += res2, modify res1
        for k, v in res2.iteritems():
            res1[k] += v

##__________________________________________________________________||
