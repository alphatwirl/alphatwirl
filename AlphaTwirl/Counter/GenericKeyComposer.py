# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class GenericKeyComposer(object):
    def __init__(self, branchNames, binnings, indices = None):
        self.branchNames = branchNames
        self.binnings = binnings
        self.indices = indices if indices is not None else [None]*len(self.branchNames)

    def begin(self, event): pass

    def __call__(self, event):
        ret = [ ]
        for varName, binning, index in zip(self.branchNames, self.binnings, self.indices):
            var = getattr(event, varName)
            if index is not None:
                if len(var) <= index: return ()
                var = var[index]
            var_bin = binning(var)
            if var_bin is None: return ()
            ret.append(var_bin)
        return (tuple(ret), )

##____________________________________________________________________________||
class GenericKeyComposerFactory(object):
    def __init__(self, branchNames, binnings, indices = None):
        self.branchNames = branchNames
        self.binnings = binnings
        self.indices = indices
    def __call__(self):
        return GenericKeyComposer(branchNames = self.branchNames, binnings = self.binnings, indices = self.indices)

##____________________________________________________________________________||
