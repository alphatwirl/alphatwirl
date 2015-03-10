# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class GenericKeyComposer(object):
    def __init__(self, varNames, binnings):
        self._varNames = varNames
        self._binnings = binnings

    def __call__(self, event):
        ret = [ ]
        for varName, binning in zip(self._varNames, self._binnings):
            var = getattr(event, varName)
            var_bin = binning(var)
            if var_bin is None: return None
            ret.append(var_bin)
        return tuple(ret)

    def binnings(self):
        return self._binnings

##____________________________________________________________________________||
