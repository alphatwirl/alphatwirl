# Tai Sakuma <tai.sakuma@cern.ch>
import itertools

from .parse_indices_config import parse_indices_config

##__________________________________________________________________||
class KeyValueComposer(object):
    """This class composes a key and a value for the event

    This class can be used with BEvents.

    This class supports inclusive indices '*'

    This class supports back references.

    (this docstring is under development.)

    """
    def __init__(self, keyAttrNames = None, binnings = None, keyIndices = None,
                 valAttrNames = None, valIndices = None):
        self.keyAttrNames = tuple(keyAttrNames) if keyAttrNames is not None else ()
        self.binnings = tuple(binnings) if binnings is not None else ()
        self.keyIndices = tuple(keyIndices) if keyIndices is not None else (None, )*len(self.keyAttrNames)
        self.valAttrNames = tuple(valAttrNames) if valAttrNames is not None else ()
        self.valIndices = tuple(valIndices) if valIndices is not None else (None, )*len(self.valAttrNames)

        if not len(self.keyAttrNames) == len(self.binnings) == len(self.keyIndices):
            raise ValueError(
                "the three tuples must have the same length: keyAttrNames = {}, binnings = {}, keyIndices = {}".format(
                    self.keyAttrNames, self.binnings, self.keyIndices
                )
            )

        if not len(self.valAttrNames) == len(self.valIndices):
            raise ValueError(
                "the two tuples must have the same length: valAttrNames = {}, valIndices = {}".format(
                    self.valAttrNames, self.valIndices
                )
            )

        self.backrefMap = { }

    def begin(self, event):
        self._zip = self._zipArrays(event)

    def __call__(self, event):
        if self._zip is None: return ()

        bins_list, vals_list = self._read_branches()
        import pprint
        print "bins_list:"
        pprint.pprint(bins_list)
        print "vals_list:"
        pprint.pprint(vals_list)
        # e.g.,
        # bins_list = [
        #     [1001],
        #     [15.0, 12.0, None, 10.0],
        #     [None, 1.2, 2.2, 0.5],
        #     [20.0, 11.0, 13.0],
        #     [2.5, None, 1.0],
        #     [0.1, 0.6, None, 0.3]
        # ]
        # vals_list = [
        #     [21.0, 13.0, 15.0, 11.0],
        #     [22.0, 15.0, 16.0]
        # ]

        if not self.useBackref:
            return self._fast_path_without_backref(bins_list, vals_list)

        # e.g.,
        # backrefIdxs = [None, None, 1, None, 3, 1, 1, 3]

        print "self.backrefIdxs:"
        pprint.pprint(self.backrefIdxs)

        idxsList_uniq, binIdxsList_referring, valIdxsList_referring = self._build_idxs_lists(bins_list, vals_list, self.backrefIdxs)
        print "idxsList_uniq:"
        pprint.pprint(idxsList_uniq)
        print "binIdxsList_referring:"
        pprint.pprint(binIdxsList_referring)
        print "valIdxsList_referring:"
        pprint.pprint(valIdxsList_referring)

        # e.g.,
        # idxsList_uniq = [
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
        #     [0, 1, 2],
        #     [0, 1, 2, 3],
        # ]
        #
        # valIdxsList_referring = [
        #     [0, 1, 2, 3],
        #     [0, 1, 2]]
        # ]
        #
        # these 5 lists are the same object:
        #   binIdxsList_uniq[1]
        #   binIdxsList_referring[1]
        #   binIdxsList_referring[2]
        #   binIdxsList_referring[5]
        #   valIdxsList_referring[0]
        #
        # so are these 3 lists:
        #   binIdxsList_uniq[2]
        #   binIdxsList_referring[3]
        #   binIdxsList_referring[4]
        #   valIdxsList_referring[1]

        print [id(o) for o in idxsList_uniq]
        print [id(o) for o in binIdxsList_referring]
        print [id(o) for o in valIdxsList_referring]

        self._remove_idxs_for_None_elements(bins_list, binIdxsList_referring)
        self._remove_idxs_for_None_elements(vals_list, valIdxsList_referring)

        print "idxsList_uniq:"
        pprint.pprint(idxsList_uniq)
        print "binIdxsList_referring:"
        pprint.pprint(binIdxsList_referring)
        print "valIdxsList_referring:"
        pprint.pprint(valIdxsList_referring)

        # e.g.,
        # idxsList_uniq = [
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
        #     [0, 2],
        # ]
        #
        # valIdxsList_referring = [
        #     [1, 3],
        #     [0, 2]
        # ]

        self._expand_idxsList_with_all_combinations(idxsList_uniq)

        print "idxsList_uniq:"
        pprint.pprint(idxsList_uniq)
        print "binIdxsList_referring:"
        pprint.pprint(binIdxsList_referring)
        print "valIdxsList_referring:"
        pprint.pprint(valIdxsList_referring)


        # e.g.,
        # idxsList_uniq = [
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
        #     [0, 2, 0, 2],
        #     [1, 1, 3, 3],
        # ]
        #
        # valIdxsList_referring = [
        #     [1, 1, 3, 3],
        #     [0, 2, 0, 2]
        # ]

        key = self._build_ret(bins_list, binIdxsList_referring) if self.keyIndices else None
        # e.g.,
        # key = (
        #     (1001, 12.0, 1.2, 20.0, 2.5, 0.6),
        #     (1001, 12.0, 1.2, 13.0, 1.0, 0.6),
        #     (1001, 10.0, 0.5, 20.0, 2.5, 0.3),
        #     (1001, 10.0, 0.5, 13.0, 1.0, 0.3)
        # )

        val = self._build_ret(vals_list, valIdxsList_referring) if self.valIndices else None
        # e.g.,
        # val = (
        #     (13.0, 22.0),
        #     (13.0, 16.0),
        #     (11.0, 22.0),
        #     (11.0, 16.0)
        # )

        return key, val

        key, val = self._build_key_val(bins_list, vals_list, binIdxsList_referring)
        # e.g.,
        # key = (
        #    (1001, 12, 1, 20, 2),
        #    (1001, 12, 1, 13, 1),
        #    (1001, 10, 0, 20, 2),
        #    (1001, 10, 0, 13, 1),
        # )

        return key, val

    def _read_branches(self):
        self.backrefMap.clear()
        bins_list = [ ]
        vals_list = [ ]
        for keyIdx, branch, binning, branchIdx, backrefIdx in self._zip:
            idxs = self._determine_branch_indices_to_read(branch, branchIdx, keyIdx, backrefIdx)
            vals = [(branch[i] if i < len(branch) else None) for i in idxs]
            if binning is not None:
                bins = [binning(val) for val in vals]
                bins_list.append(bins)
            else:
                vals_list.append(vals)
        return bins_list, vals_list

    def _determine_branch_indices_to_read(self, branch, branchIdx, keyIdx, backrefIdx):
        if backrefIdx is None:
            if branchIdx == '*': ret = range(len(branch))
            elif branchIdx < len(branch): ret = [branchIdx]
            else: ret = [ ]
        else:
            ret = self.backrefMap[backrefIdx]
        self.backrefMap[keyIdx] = ret
        return ret

    def _fast_path_without_backref(self, bins_list, vals_list):
        for bins in bins_list:
            bins[:] = [b for b in bins if b is not None]
        for vals in vals_list:
            vals[:] = [v for v in vals if v is not None]
        prod = tuple(itertools.product(*(bins_list + vals_list)))
        keys = tuple(e[0:len(bins_list)] for e in prod) if bins_list else None
        vals = tuple(e[len(bins_list):] for e in prod) if vals_list else None
        return keys, vals

    def _build_idxs_lists(self, bins_list, vals_list, backrefIdxs):
        uniq_list, referring_list = self._build_binIdxs_lists(bins_list + vals_list, backrefIdxs)
        return uniq_list, referring_list[:len(bins_list)], referring_list[len(bins_list):]

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

    def _remove_idxs_for_None_elements(self, bins_list, idxsList):
        for bins, idxs in zip(bins_list, idxsList):
            idxsToRemove = [i for i, b in enumerate(bins) if b is None]
            idxs[:] = [i for i in idxs if i not in idxsToRemove]

    def _expand_idxsList_with_all_combinations(self, IdxsList):
        prod = tuple(itertools.product(*IdxsList))
        for i in range(len(IdxsList)):
            IdxsList[i][:] = [p[i] for p in prod]

    def _build_ret(self, bins_list, idxsList):
        if not idxsList: return tuple()
        ret = [ ]
        for i in range(len(idxsList[0])):
            ret.append(tuple([b[idxs[i]] for b, idxs in zip(bins_list, idxsList)]))
        val = [ ]
        return tuple(ret)

    def _zipArrays(self, event):
        attrs = [ ]
        for varname in self.keyAttrNames + self.valAttrNames:
            try:
                branch = getattr(event, varname)
            except AttributeError, e:
                import logging
                logging.warning(e)
                return None
            attrs.append(branch)
        indices = self.keyIndices + self.valIndices
        self.backrefIdxs, indices = parse_indices_config(indices)
        self.useBackref = any([e is not None for e in self.backrefIdxs])
        self.keyIdxs = range(len(attrs))
        binnings = self.binnings + (None, )*len(self.valAttrNames)
        return zip(self.keyIdxs, attrs, binnings, indices, self.backrefIdxs)

##__________________________________________________________________||
