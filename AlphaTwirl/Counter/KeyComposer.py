# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class GenericKeyComposer(object):
    def __init__(self, varNames, binnings, indices = None):
        self._varNames = varNames
        self._binnings = binnings
        self._indices = indices if indices is not None else [None]*len(self._varNames)

    def __call__(self, event):
        ret = [ ]
        for varName, binning, index in zip(self._varNames, self._binnings, self._indices):
            var = getattr(event, varName)
            if index is not None:
                if len(var) <= index: return None
                var = var[index]
            var_bin = binning(var)
            if var_bin is None: return None
            ret.append(var_bin)
        return tuple(ret)

    def next(self, key):
        ret = [ ]
        for i in range(len(self._binnings)):
            keyc = list(key)
            keyc[i] = self._binnings[i].next(keyc[i])
            ret.append(tuple(keyc))
        return tuple(ret)

    def binnings(self):
        return self._binnings

##____________________________________________________________________________||
class GenericKeyComposerBuilder(object):
    def __init__(self, varNames, binnings, indices = None):
        self.varNames = varNames
        self.binnings = binnings
        self.indices = indices
    def __call__(self):
        return GenericKeyComposer(varNames = self.varNames, binnings = self.binnings, indices = self.indices)

##____________________________________________________________________________||
