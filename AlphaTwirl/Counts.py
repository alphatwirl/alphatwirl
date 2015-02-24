# Tai Sakuma <sakuma@fnal.gov>
import pandas

##____________________________________________________________________________||
class Counts(object):
    def __init__(self):
        self._counts = { }

    def count(self, key, w = 1, nvar = None):
        if nvar is None: nvar = w**2
        if key not in self._counts: self._counts[key] = {'n': 0.0, 'nvar': 0.0 }
        self._counts[key]['n'] += w
        self._counts[key]['nvar'] += nvar

    def results(self):
        return self._counts

##____________________________________________________________________________||
def countsToDataFrame(counts, keyNames, valNames = ('n', 'nvar')):
    columns = tuple(keyNames) + tuple(valNames)
    if not counts:
        return pandas.DataFrame(columns = columns)
        return
    d = [k + (v['n'], v['nvar']) for k, v in counts.iteritems()]
    d.sort()
    return pandas.DataFrame(d, columns = columns)

##____________________________________________________________________________||
