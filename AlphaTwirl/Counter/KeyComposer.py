# Tai Sakuma <sakuma@fnal.gov>

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

    def binnings(self):
        return self._binnings

##____________________________________________________________________________||
