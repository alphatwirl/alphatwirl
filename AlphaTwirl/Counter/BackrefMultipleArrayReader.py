# Tai Sakuma <tai.sakuma@cern.ch>
import itertools

##__________________________________________________________________||
class BackrefMultipleArrayReader(object):
    def __init__(self, arrays, idxs_conf, backref_idxs):
        self.backref_idxs = backref_idxs
        self._use_backref = any([e is not None for e in backref_idxs])
        self._zipped = zip(range(len(arrays)), arrays, idxs_conf, backref_idxs)

        self.arrays = arrays

    def read(self):
        return self._read_zipped(self._zipped, self.backref_idxs)

    def _read_zipped(self, zipped, backref_idxs):

        varis = self._unzip_and_read_arrays(zipped)
        # e.g.,
        # varis = [
        #     [1001],
        #     [15.3, 12.9, 9.2, 10.5],
        #     [-1.2, 5.2, 2.2, 0.5],
        #     [20.2, 11.9, 13.3, 5.2],
        #     [2.2, 1.2, -1.5, -0.5],
        #     [0.1, 0.6, 1.2, None],
        #     [16.2, 13.1, 10.1, 11.8],
        #     [22.1, 15.2, 16.3, None]
        # ]

        if not self._use_backref:
            # fast path without backref
            return tuple(itertools.product(*varis))

        # e.g.,
        # backref_idxs = [None, None, 1, None, 3, 1, 1, 3]

        uniq_idxs, ref_key_idxs = self._build_uniq_ref_idxs(varis, backref_idxs)
        # e.g.,
        # uniq_idxs = [
        #     [0],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3]
        # ]
        #
        # ref_key_idxs = [
        #     [0],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        # ]
        #
        # these 5 lists are the same object:
        #   uniq_idxs[1]
        #   ref_key_idxs[1]
        #   ref_key_idxs[2]
        #   ref_key_idxs[5]
        #   ref_key_idxs[]
        #
        # so are these 3 lists:
        #   uniq_idxs[2]
        #   ref_key_idxs[3]
        #   ref_key_idxs[4]
        #   ref_key_idxs[7]

        self._expand_idxs_with_all_combinations(uniq_idxs)
        # e.g.,
        # uniq_idxs = [
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        #     [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        # ]
        #
        # e.g.,
        # ref_key_idxs = [
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        #     [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        #     [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
        #     [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
        #     [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        #     [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        #     [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        # ]

        varis = self._build_ret(varis, ref_key_idxs)
        # e.g.,
        # varis = (
        #     (1001, 15.3, -1.2, 20.2, 2.2, 0.1, 16.2, 22.1),
        #     (1001, 15.3, -1.2, 11.9, 1.2, 0.1, 16.2, 15.2),
        #     (1001, 15.3, -1.2, 13.3, -1.5, 0.1, 16.2, 16.3),
        #     (1001, 15.3, -1.2, 5.2, -0.5, 0.1, 16.2, None),
        #     (1001, 12.9, 5.2, 20.2, 2.2, 0.6, 13.1, 22.1),
        #     (1001, 12.9, 5.2, 11.9, 1.2, 0.6, 13.1, 15.2),
        #     (1001, 12.9, 5.2, 13.3, -1.5, 0.6, 13.1, 16.3),
        #     (1001, 12.9, 5.2, 5.2, -0.5, 0.6, 13.1, None),
        #     (1001, 9.2, 2.2, 20.2, 2.2, 1.2, 10.1, 22.1),
        #     (1001, 9.2, 2.2, 11.9, 1.2, 1.2, 10.1, 15.2),
        #     (1001, 9.2, 2.2, 13.3, -1.5, 1.2, 10.1, 16.3),
        #     (1001, 9.2, 2.2, 5.2, -0.5, 1.2, 10.1, None),
        #     (1001, 10.5, 0.5, 20.2, 2.2, None, 11.8, 22.1),
        #     (1001, 10.5, 0.5, 11.9, 1.2, None, 11.8, 15.2),
        #     (1001, 10.5, 0.5, 13.3, -1.5, None, 11.8, 16.3),
        #     (1001, 10.5, 0.5, 5.2, -0.5, None, 11.8, None)
        # )

        return varis

    def _unzip_and_read_arrays(self, zipped):
        backref_map = { }
        varis = [ ]
        for var_idx, attr, conf_attr_idx, backref_idx in zipped:
            attr_idxs = self._determine_array_indices_to_read(attr, conf_attr_idx, var_idx, backref_idx, backref_map)
            attr_vals = [(attr[i] if i < len(attr) else None) for i in attr_idxs]
            varis.append(attr_vals)
        return varis

    def _determine_array_indices_to_read(self, attr, conf_attr_idx, var_idx, backref_idx, backref_map):
        if backref_idx is None:
            if conf_attr_idx == '*': ret = range(len(attr))
            elif conf_attr_idx < len(attr): ret = [conf_attr_idx]
            else: ret = [ ] # conf_attr_idx is out of the range
        else:
            ret = backref_map[backref_idx]
        backref_map[var_idx] = ret
        return ret

    def _build_uniq_ref_idxs(self, keys, backref_idxs):
        uniq_idxs = [ ]
        ref_idxs = [ ]
        for keys, backrefIdx in zip(keys, backref_idxs):
            if backrefIdx is None:
                idxs = range(len(keys))
                uniq_idxs.append(idxs)
                ref_idxs.append(idxs)
            else:
                ref_idxs.append(ref_idxs[backrefIdx])
        return uniq_idxs, ref_idxs

    def _expand_idxs_with_all_combinations(self, idxs):
        prod = tuple(itertools.product(*idxs))
        for i in range(len(idxs)):
            idxs[i][:] = [p[i] for p in prod]

    def _build_ret(self, varis, idxs):
        if not idxs: return tuple()
        ret = [ ]
        for i in range(len(idxs[0])):
            ret.append(tuple([b[subidxs[i]] for b, subidxs in zip(varis, idxs)]))
        val = [ ]
        return tuple(ret)
##__________________________________________________________________||
