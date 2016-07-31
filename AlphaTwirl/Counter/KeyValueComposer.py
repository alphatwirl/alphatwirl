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

    def begin(self, event):
        attr_names = self.keyAttrNames + self.valAttrNames
        idxs_conf = self.keyIndices + self.valIndices
        self.backref_idxs, idxs_conf = parse_indices_config(idxs_conf)
        arrays = self._collect_arrays(event,  attr_names) 

        self._active = True if arrays else False

        self._use_backref = any([e is not None for e in self.backref_idxs])

        self._zipped = self._zip_arrays(arrays, idxs_conf, self.backref_idxs) if arrays is not None else None

    def _collect_arrays(self, event, attr_names):
        ret = [ ]
        for varname in attr_names:
            try:
                attr = getattr(event, varname)
            except AttributeError, e:
                import logging
                logging.warning(e)
                return None
            ret.append(attr)
        return ret

    def _zip_arrays(self, arrays, idxs_conf, backref_idxs):
        self._array_reader = BackrefMultipleArrayReader(arrays, idxs_conf, backref_idxs)
        array_idxs = range(len(arrays))
        return zip(array_idxs, arrays, idxs_conf, backref_idxs)

    def __call__(self, event):
        if not self._active: return None, None

        varis = self._array_reader.read()

        # if self._zipped is None: return ()
        # varis = self._read_zipped(self._zipped, self.backref_idxs)
        key, val =  self._seprate_into_keys_and_vals_2(varis)
        key = self._apply_binnings(self.binnings, key)
        key, val = self._remove_None(key, val)
        return key, val

    def _seprate_into_keys_and_vals_2(self, varis):
        key = [v[:len(self.keyAttrNames)] for v in varis] if self.keyAttrNames else None
        val = [v[len(self.keyAttrNames):] for v in varis] if self.valAttrNames else None
        return key, val

    def _apply_binnings(self, binnings, keys):
        if keys is None: return None
        return tuple(tuple(b(k) for b, k in zip(binnings, kk)) for kk in keys)

    def _remove_None(self, key, val):
        if key is None:
            if val is None:
                return key, val
            else:
                idxs = tuple(i for i, e in enumerate(val) if None not in e)
                val = tuple(val[i] for i in idxs)
                return key, val
        else:
            if val is None:
                idxs = tuple(i for i, e in enumerate(key) if None not in e)
                key = tuple(key[i] for i in idxs)
                return key, val
            else:
                idxs_key = set(i for i, e in enumerate(key) if None not in e)
                idxs_val = set(i for i, e in enumerate(val) if None not in e)
                idxs = idxs_key & idxs_val # intersection
                idxs = sorted(list(idxs))
                key = tuple(key[i] for i in idxs)
                val = tuple(val[i] for i in idxs)
                return key, val

##__________________________________________________________________||
class BackrefMultipleArrayReader(object):
    def __init__(self, arrays, idxs_conf, backref_idxs):
        self.backref_idxs = backref_idxs
        self._use_backref = any([e is not None for e in backref_idxs])
        self._zipped = zip(range(len(arrays)), arrays, idxs_conf, backref_idxs)

    def read(self):
        return self._read_zipped(self._zipped, self.backref_idxs)

    def _read_zipped(self, zipped, backref_idxs):

        varis = self._unzip_and_read_event_attributes(zipped)

        if not self._use_backref:
            return self._fast_path_without_backref(varis)

        # e.g.,
        # keys = [
        #     [1001],
        #     [15.0, 12.0, None, 10.0],
        #     [None, 1.2, 2.2, 0.5],
        #     [20.0, 11.0, 13.0],
        #     [2.5, None, 1.0],
        #     [0.1, 0.6, None, 0.3]
        # ]
        # vals = [
        #     [21.0, 13.0, 15.0, 11.0],
        #     [22.0, 15.0, 16.0]
        # ]


        # e.g.,
        # backref_idxs = [None, None, 1, None, 3, 1, 1, 3]

        uniq_idxs, ref_key_idxs = self._build_uniq_ref_idxs(varis, backref_idxs)
        # e.g.,
        # uniq_idxs = [
        #     [0],
        #     [0, 1, 2, 3],
        #     [0, 1, 2]
        # ]
        #
        # ref_key_idxs = [
        #     [0],
        #     [0, 1, 2, 3],
        #     [0, 1, 2, 3],
        #     [0, 1, 2],
        #     [0, 1, 2],
        #     [0, 1, 2, 3],
        # ]
        #
        # ref_val_idxs = [
        #     [0, 1, 2, 3],
        #     [0, 1, 2]]
        # ]
        #
        # these 5 lists are the same object:
        #   binIdxsList_uniq[1]
        #   ref_key_idxs[1]
        #   ref_key_idxs[2]
        #   ref_key_idxs[5]
        #   ref_val_idxs[0]
        #
        # so are these 3 lists:
        #   binIdxsList_uniq[2]
        #   ref_key_idxs[3]
        #   ref_key_idxs[4]
        #   ref_val_idxs[1]

        # e.g.,
        # uniq_idxs = [
        #     [0],
        #     [1, 3],
        #     [0, 2]
        # ]
        #
        # ref_key_idxs = [
        #     [0],
        #     [1, 3],
        #     [1, 3],
        #     [0, 2],
        #     [0, 2],
        # ]
        #
        # ref_val_idxs = [
        #     [1, 3],
        #     [0, 2]
        # ]

        self._expand_idxs_with_all_combinations(uniq_idxs)
        # e.g.,
        # uniq_idxs = [
        #     [0, 0, 0, 0],
        #     [1, 1, 3, 3],
        #     [0, 2, 0, 2]
        # ]
        #
        # ref_key_idxs = [
        #     [0, 0, 0, 0],
        #     [1, 1, 3, 3],
        #     [1, 1, 3, 3],
        #     [0, 2, 0, 2],
        #     [0, 2, 0, 2],
        #     [1, 1, 3, 3],
        # ]
        #
        # ref_val_idxs = [
        #     [1, 1, 3, 3],
        #     [0, 2, 0, 2]
        # ]

        varis = self._build_ret(varis, ref_key_idxs)
        return varis

    def _unzip_and_read_event_attributes(self, zipped):
        backref_map = { }
        varis = [ ]
        for var_idx, attr, conf_attr_idx, backref_idx in zipped:
            attr_idxs = self._determine_attr_indices_to_read(attr, conf_attr_idx, var_idx, backref_idx, backref_map)
            attr_vals = [(attr[i] if i < len(attr) else None) for i in attr_idxs]
            varis.append(attr_vals)
        return varis

    def _determine_attr_indices_to_read(self, attr, conf_attr_idx, var_idx, backref_idx, backref_map):
        if backref_idx is None:
            if conf_attr_idx == '*': ret = range(len(attr))
            elif conf_attr_idx < len(attr): ret = [conf_attr_idx]
            else: ret = [ ] # conf_attr_idx is out of the range
        else:
            ret = backref_map[backref_idx]
        backref_map[var_idx] = ret
        return ret

    def _fast_path_without_backref(self, varis):
        varis = tuple(itertools.product(*varis))
        return varis

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
