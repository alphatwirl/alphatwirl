# Tai Sakuma <tai.sakuma@cern.ch>
import itertools

##__________________________________________________________________||
class GenericKeyComposerB(object):
    """This class is a faster version of GenericKeyComposer.

    This class can be used with BEvents.

    This class supports inclusive indices '*'

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
        bins_list = [ ]
        for branche, binning, index in self._zip:
            bins = self._bins(branche, binning, index)
            if not bins: return ()
            bins_list.append(bins)
        return tuple(itertools.product(*bins_list))

    def _bins(self, branche, binning, index):
        if index is None:
            vars = [branche[0]]
        elif index == '*':
            vars = [branche[i] for i in  range(len(branche))]
        else:
            if len(branche) <= index:
                vars = [ ]
            else:
                vars = [branche[index]]
        bins = [binning(var) for var in vars]
        bins = [b for b in bins if b is not None]
        return bins

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

##__________________________________________________________________||
