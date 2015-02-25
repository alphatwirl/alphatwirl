# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class Counts(object):
    def __init__(self):
        self._counts = { }

    def count(self, key, w = 1, nvar = None):
        if nvar is None: nvar = w**2
        if key not in self._counts: self._counts[key] = {'n': 0.0, 'nvar': 0.0 }
        self._counts[key]['n'] += w
        self._counts[key]['nvar'] += nvar

    def valNames(self):
        return ('n', 'nvar')

    def results(self):
        return self._counts

##____________________________________________________________________________||
