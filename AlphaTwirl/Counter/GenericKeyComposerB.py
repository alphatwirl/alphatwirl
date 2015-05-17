# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class GenericKeyComposerB(object):
    def __init__(self, varNames, binnings, indices = None):
        self._varNames = varNames
        self._binnings = binnings
        self._indices = indices if indices is not None else [None]*len(self._varNames)
        self._first = True

    def __call__(self, event):
        if self._first:
            self._findArrays(event)
            self._first = False

        if self._zip is None: return None

        ret = [ ]
        for branche, binning, index in self._zip:
            if index is not None:
                if len(branche) <= index: return None
                var = branche[index]
            else:
                var = branche[0]
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

    def _findArrays(self, event):
        self._branches = [ ]
        for varname in self._varNames:
            try:
                branch = getattr(event, varname)
            except AttributeError, e:
                import logging
                logging.warning(e)
                self._zip = None
                return
            self._branches.append(branch)
        self._zip = zip(self._branches, self._binnings, self._indices)

##____________________________________________________________________________||
class GenericKeyComposerBBuilder(object):
    def __init__(self, varNames, binnings, indices = None):
        self.varNames = varNames
        self.binnings = binnings
        self.indices = indices
    def __call__(self):
        return GenericKeyComposerB(varNames = self.varNames, binnings = self.binnings, indices = self.indices)

##____________________________________________________________________________||
