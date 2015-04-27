# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class GenericKeyComposerAddressAccess(object):
    def __init__(self, varNames, binnings, indices = None):
        self._varNames = varNames
        self._binnings = binnings
        self._indices = indices if indices is not None else [None]*len(self._varNames)
        self._first = True

    def __call__(self, event):
        if self._first:
            self._findArrays(event)
            self._first = False

        ret = [ ]
        for array, binning, index, countarray in self._zip:
            if index is not None:
                if countarray[0] <= index: return None
                var = array[index]
            else:
                var = array[0]
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
        self._arrays = [event.arrays[n]['array'] for n in self._varNames]
        self._countarrays = [event.arrays[n]['countarray'] for n in self._varNames]
        self._zip = zip(self._arrays, self._binnings, self._indices, self._countarrays)

##____________________________________________________________________________||
class GenericKeyComposerAddressAccessBuilder(object):
    def __init__(self, varNames, binnings, indices = None):
        self.varNames = varNames
        self.binnings = binnings
        self.indices = indices
    def __call__(self):
        return GenericKeyComposerAddressAccess(varNames = self.varNames, binnings = self.binnings, indices = self.indices)

##____________________________________________________________________________||
