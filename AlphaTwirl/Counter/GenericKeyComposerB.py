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

        self.backrefMap = { }

    def begin(self, event):
        self._zip = self._zipArrays(event)

    def __call__(self, event):
        if self._zip is None: return ()
        bins_list = [ ]
        binIdxMap = { }
        self.backrefMap.clear()
        for keyIdx, branch, binning, branchIdx, idxCite in self._zip:
            idxs = self._determine_branch_indices_to_read(branch, branchIdx, keyIdx, idxCite)
            vals = self._vals(branch, idxs)
            bins = self._bins(binning, vals)
            bins_list.append(bins)

        idxs_list = [ ]
        idxs_list_u = [ ]
        for bins, idxCite in zip(bins_list, self.idxCites):
            if idxCite is None:
                idxs = range(len(bins))
                idxs_list.append(idxs)
                idxs_list_u.append(idxs)
            else:
                idxs_list.append(idxs_list[idxCite])

        for bins, idxs in zip(bins_list, idxs_list):
            idxsToRemove = [i for i, b in enumerate(bins) if b is None]
            idxs[:] = [i for i in idxs if i not in idxsToRemove]

        idxs_list_v = tuple(itertools.product(*idxs_list_u))
        for i in range(len(idxs_list_u)):
            idxs_list_u[i][:] = [j[i] for j in  idxs_list_v]
        ret = [ ]
        for i in range(len(idxs_list[0])):
            ret.append(tuple([b[idxs[i]] for b, idxs in zip(bins_list, idxs_list)]))
        return tuple(ret)

    def _determine_branch_indices_to_read(self, branch, index, keyIdx, idxCite):
        if idxCite is None:
            if index == '*': ret = range(len(branch))
            elif index < len(branch): ret = [index]
            else: ret = [ ]
        else:
            ret = self.backrefMap[idxCite]
        self.backrefMap[keyIdx] = ret
        return ret

    def _vals(self, branch, idxs):
        return [branch[i] for i in idxs]

    def _bins(self, binning, vals):
        bins = [binning(val) for val in vals]
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
        self.idxCites, self.indices = self._parse_indices_config(self.indices)
        self.keyIdxs = range(len(self.branches))
        return zip(self.keyIdxs, self.branches, self.binnings, self.indices, self.idxCites)

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

        indices = [i if c is None else c for i, c in zip(indices, idxCites)]
        # e.g., [0, '*', '*', -2, -3]

        return idxCites, indices

##__________________________________________________________________||
