# Tai Sakuma <tai.sakuma@cern.ch>
import itertools
import re

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
        for branch, binning, index in self._zip:
            idxs = self._idxs(branch, index)
            vals = self._vals(branch, idxs)
            bins = self._bins(binning, vals)
            if not bins: return ()
            bins_list.append(bins)
        return tuple(itertools.product(*bins_list))

    def _idxs(self, branch, index):
        if index == '*': return range(len(branch))
        if index < len(branch): return [index]
        return [ ]

    def _vals(self, branch, idxs):
        return [branch[i] for i in idxs]

    def _bins(self, binning, vals):
        bins = [binning(val) for val in vals]
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
        indices = self._parse_indices_config(self.indices)
        return zip(self.branches, self.binnings, indices)

    def _parse_indices_config(self, indices):
        indices = list(indices)

        # indices e.g., [None, None, '(*)', '(*)', '\\1', '\\2']

        # replace None with 0
        indices = [0 if i is None else i for i in indices]
        # e.g., [0, 0, '(*)', '(*)', '\\1', '\\2']

        # search for elements in parentheses, e.g. '(*)'
        # at the momentum, only the asterisk '*' can be in the parentheses
        idxRefs = [re.search(r'^\((.*)\)$', i) if isinstance(i, basestring) else None for i in indices]
        # e.g., [None, None, <Match object>, <Match object>, None, None]

        # remove parentheses
        indices = [r.group(1) if r else i for i, r in zip(indices, idxRefs)]
        # e.g., [0, 0, '*', '*', '\\1', '\\2']

        ref = 1
        for i, v in enumerate(idxRefs):
            if v:
                idxRefs[i] = ref
                ref += 1
        # e.g., idxRefs  = [None, None, 1, 2, None, None]

        idxCites = [int(i[1:]) if isinstance(i, basestring) and i.startswith('\\') else None for i in indices]
        # e.g., [None, None, None, None, 1, 2] # the original refs

        idxCites = [None if i is None else idxRefs.index(i) for i in idxCites]
        # e.g., [None, None, None, None, 2, 3] # indices in the list indices

        # use negative numbers, to distinguish from the real indices
        idxCites = [None if i is None else -i for i in idxCites]
        # e.g., [None, None, None, None, -2, -3]

        indices = [i if c is None else c for i, c in zip(indices, idxCites)]
        # e.g., [0, '*', '*', -2, -3]

        return indices

##__________________________________________________________________||
