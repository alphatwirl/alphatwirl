# Tai Sakuma <tai.sakuma@cern.ch>
import itertools
import re

##__________________________________________________________________||
class GenericKeyComposerB(object):
    """This class is a faster version of GenericKeyComposer.

    This class can be used with BEvents.

    This class supports inclusive indices '*'

    This class supports back references.

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

        bins_list = self._read_branches()
        # e.g.,
        # bins_list = [
        #     [1001],
        #     [15, 12, None, 10],
        #     [None, 1, 2, 0],
        #     [20, 11, 13],
        #     [2, None, 1]
        # ]

        if not self.useBackref:
            return self._fast_path_without_backref(bins_list)

        binIdxsList_uniq, binIdxsList_referring = self._build_binIdxs_lists(bins_list, self.backrefIdxs)
        # e.g., backrefIdxs = [None, None, 1, None, 3]
        # binIdxsList_uniq = [
        #     [0],
        #     [0, 1, 2, 3],
        #     [0, 1, 2]
        # ]
        #
        # binIdxsList_referring = [
        #     [0],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        #     [0, 1, 2],
        #     [0, 1, 2]
        # ]
        #
        # these 3 lists are the same object:
        #   binIdxsList_uniq[1]
        #   binIdxsList_referring[1]
        #   binIdxsList_referring[2]
        #
        # so are these 3 lists:
        #   binIdxsList_uniq[2]
        #   binIdxsList_referring[3]
        #   binIdxsList_referring[4]

        self._remove_binIdxs_for_None_elements(bins_list, binIdxsList_referring)
        # e.g.,
        # binIdxsList_uniq = [
        #     [0],
        #     [1, 3],
        #     [0, 2]
        # ]
        #
        # binIdxsList_referring = [
        #     [0],
        #     [1, 3],
        #     [1, 3],
        #     [0, 2],
        #     [0, 2]
        # ]

        self._expand_idxsList_with_all_combinations(binIdxsList_uniq)
        # e.g.,
        # binIdxsList_uniq = [
        #     [0, 0, 0, 0],
        #     [1, 1, 3, 3],
        #     [0, 2, 0, 2]
        # ]
        #
        # binIdxsList_referring = [
        #     [0, 0, 0, 0],
        #     [1, 1, 3, 3],
        #     [1, 1, 3, 3],
        #     [0, 2, 0, 2],
        #     [0, 2, 0, 2]
        # ]


        key = self._build_key(bins_list, binIdxsList_referring)
        # e.g.,
        # key = (
        #    (1001, 12, 1, 20, 2),
        #    (1001, 12, 1, 13, 1),
        #    (1001, 10, 0, 20, 2),
        #    (1001, 10, 0, 13, 1),
        # )

        return key

    def _read_branches(self):
        self.backrefMap.clear()
        bins_list = [ ]
        for keyIdx, branch, binning, branchIdx, backrefIdx in self._zip:
            idxs = self._determine_branch_indices_to_read(branch, branchIdx, keyIdx, backrefIdx)
            vals = [branch[i] for i in idxs]
            bins = [binning(val) for val in vals]
            bins_list.append(bins)
        return bins_list

    def _determine_branch_indices_to_read(self, branch, branchIdx, keyIdx, backrefIdx):
        if backrefIdx is None:
            if branchIdx == '*': ret = range(len(branch))
            elif branchIdx < len(branch): ret = [branchIdx]
            else: ret = [ ]
        else:
            ret = self.backrefMap[backrefIdx]
        self.backrefMap[keyIdx] = ret
        return ret

    def _fast_path_without_backref(self, bins_list):
        for bins in bins_list:
            bins[:] = [b for b in bins if b is not None]
        return tuple(itertools.product(*bins_list))

    def _build_binIdxs_lists(self, bins_list, backrefIdxs):
        uniq_list = [ ]
        referring_list = [ ]
        for bins, backrefIdx in zip(bins_list, backrefIdxs):
            if backrefIdx is None:
                idxs = range(len(bins))
                uniq_list.append(idxs)
                referring_list.append(idxs)
            else:
                referring_list.append(referring_list[backrefIdx])
        return uniq_list, referring_list

    def _remove_binIdxs_for_None_elements(self, bins_list, binIdxsList):
        for bins, idxs in zip(bins_list, binIdxsList):
            idxsToRemove = [i for i, b in enumerate(bins) if b is None]
            idxs[:] = [i for i in idxs if i not in idxsToRemove]

    def _expand_idxsList_with_all_combinations(self, IdxsList):
        prod = tuple(itertools.product(*IdxsList))
        for i in range(len(IdxsList)):
            IdxsList[i][:] = [p[i] for p in prod]

    def _build_key(self, bins_list, binIdxsList):
        if not binIdxsList: return tuple()
        ret = [ ]
        for i in range(len(binIdxsList[0])):
            ret.append(tuple([b[idxs[i]] for b, idxs in zip(bins_list, binIdxsList)]))
        return tuple(ret)

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
        self.backrefIdxs, self.indices = parse_indices_config(self.indices)
        self.useBackref = any([e is not None for e in self.backrefIdxs])
        self.keyIdxs = range(len(self.branches))
        return zip(self.keyIdxs, self.branches, self.binnings, self.indices, self.backrefIdxs)

##__________________________________________________________________||
def parse_indices_config(indices):
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

    backrefIdxs = [int(i[1:]) if isinstance(i, basestring) and i.startswith('\\') else None for i in indices]
    # e.g., [None, None, None, None, 1, 2] # the original refs

    backrefIdxs = [None if i is None else idxRefs.index(i) for i in backrefIdxs]
    # e.g., [None, None, None, None, 2, 3] # indices in the list "indices"

    # e.g.:
    # backrefIdxs = [None, None, None, None, 2, 3]
    # indices = [0, 0, '*', '*', '\\1', '\\2']
    return backrefIdxs, indices

##__________________________________________________________________||
