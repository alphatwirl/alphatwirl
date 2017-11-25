# Tai Sakuma <tai.sakuma@cern.ch>

import collections
import itertools
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

    def __copy__(self):
        ret = self.__class__(self.Summary)
        self._add_results_inplace(ret._results, self._results)
        return ret

    def __add__(self, other):
        ret = copy.copy(self)
        if not other == 0: # other is 0 when e.g. sum([obj1, obj2])
            self._add_results_inplace(ret._results, other._results)
        return ret

    def __iadd__(self, other):
        self._add_results_inplace(self._results, other._results)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def _add_results_inplace(self, res1, res2):
        # res1 += res2, modify res1
        for k, v in res2.items():
            res1[k] += v

    def results(self):
        return self._results

    def to_key_vals_dict(self):
        keys_sorted = sorted(self._results.keys())
        ret = collections.OrderedDict([(k, self._results[k].contents) for k in keys_sorted])
        # e.g.,
        # OrderedDict([
        #     ((200, 2), [array([120, 240])]),
        #     ((300, 2), [array([490, 980])]),
        #     ((300, 3), [array([210, 420])])
        # ])
        return ret

    def to_tuple_list(self):
        key_vals_dict = self.to_key_vals_dict()
        ret = convert_key_vals_dict_to_tuple_list(key_vals_dict, fill = 0)
        # e.g.,
        # [
        #     (200, 2, 120, 240),
        #     (300, 2, 490, 980),
        #     (300, 3, 210, 420)
        # ]
        return ret

##__________________________________________________________________||
def convert_key_vals_dict_to_tuple_list(dict_, fill = float('nan')):

    d = [ ]

    if not dict_: return d

    vlen = max([len(vs) for vs in itertools.chain(*dict_.values())])

    for k, vs in dict_.items():
        try:
            d.extend([k + tuple(v) + (fill, )*(vlen - len(v)) for v in vs])
        except TypeError:
            # assume k is not a tuple
            d.extend([(k, ) + tuple(v) + (fill, )*(vlen - len(v)) for v in vs])


    return d

##__________________________________________________________________||
