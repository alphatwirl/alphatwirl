# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class GenericKeyComposerB(object):
    def __init__(self, varNames, binnings, indices = None):
        self._varNames = varNames
        self._binnings = binnings
        self._indices = indices if indices is not None else [None]*len(self._varNames)

    def begin(self, event):
        self._zip = self._zipArrays(event)

    def __call__(self, event):
        if self._zip is None: return ()
        ret = [ ]
        for branche, binning, index in self._zip:
            if index is not None:
                if len(branche) <= index: return ()
                var = branche[index]
            else:
                var = branche[0]
            var_bin = binning(var)
            if var_bin is None: return ()
            ret.append(var_bin)
        return (tuple(ret), )

    def next(self, key):
        """returns a list of the next keys

        e.g.,
        If key = (11, 8, 20)
        it returns ((12, 8, 20), (11, 9, 20), (11, 8, 21))
        """
        ret = [ ]
        for i in range(len(self._binnings)):
            keyc = list(key)
            keyc[i] = self._binnings[i].next(keyc[i])
            ret.append(tuple(keyc))
        return tuple(ret)

    def binnings(self):
        return self._binnings

    def _zipArrays(self, event):
        self._branches = [ ]
        for varname in self._varNames:
            try:
                branch = getattr(event, varname)
            except AttributeError, e:
                import logging
                logging.warning(e)
                return None
            self._branches.append(branch)
        return zip(self._branches, self._binnings, self._indices)

##____________________________________________________________________________||
class GenericKeyComposerBBuilder(object):
    def __init__(self, varNames, binnings, indices = None):
        self.varNames = varNames
        self.binnings = binnings
        self.indices = indices
    def __call__(self):
        return GenericKeyComposerB(varNames = self.varNames, binnings = self.binnings, indices = self.indices)

##____________________________________________________________________________||
