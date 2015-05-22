# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class GenericKeyComposerB(object):
    """This class is a faster version of GenericKeyComposer.

    This class can be used with BEvents.

    (this docstring is under development.)

    """
    def __init__(self, branchNames, binnings, indices = None):
        self.branchNames = branchNames
        self.binnings = binnings
        self.indices = indices if indices is not None else [None]*len(self.branchNames)

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

    def _zipArrays(self, event):
        self.branches = [ ]
        for varname in self.branchNames:
            try:
                branch = getattr(event, varname)
            except AttributeError, e:
                import logging
                logging.warning(e)
                return None
            self.branches.append(branch)
        return zip(self.branches, self.binnings, self.indices)

##____________________________________________________________________________||
class GenericKeyComposerBFactory(object):
    def __init__(self, branchNames, binnings, indices = None):
        self.branchNames = branchNames
        self.binnings = binnings
        self.indices = indices
    def __call__(self):
        return GenericKeyComposerB(branchNames = self.branchNames, binnings = self.binnings, indices = self.indices)

##____________________________________________________________________________||
