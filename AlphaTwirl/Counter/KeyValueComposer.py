# Tai Sakuma <tai.sakuma@cern.ch>
from .parse_indices_config import parse_indices_config
from .BackrefMultipleArrayReader import BackrefMultipleArrayReader

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
        backref_idxs, idxs_conf = parse_indices_config(idxs_conf)
        arrays = self._collect_arrays(event,  attr_names)

        self._active = True if arrays else False
        self._array_reader = BackrefMultipleArrayReader(arrays, idxs_conf, backref_idxs)

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

    def __call__(self, event):
        if not self._active: return None, None
        varis = self._array_reader.read()
        key, val =  self._seprate_into_keys_and_vals(varis)
        key = self._apply_binnings(self.binnings, key)
        key, val = self._remove_None(key, val)
        return key, val

    def _seprate_into_keys_and_vals(self, varis):
        key = [v[:len(self.keyAttrNames)] for v in varis] if self.keyAttrNames else None
        val = [v[len(self.keyAttrNames):] for v in varis] if self.valAttrNames else None
        return key, val

    def _apply_binnings(self, binnings, keys):
        if keys is None: return None
        return tuple(tuple(b(k) for b, k in zip(binnings, kk)) for kk in keys)

    def _remove_None(self, key, val):
        if key is None and val is None:
            return key, val

        if key is None and val is not None:
            idxs = tuple(i for i, e in enumerate(val) if None not in e)
            val = tuple(val[i] for i in idxs)
            return key, val

        if key is not None and val is None:
            idxs = tuple(i for i, e in enumerate(key) if None not in e)
            key = tuple(key[i] for i in idxs)
            return key, val

        idxs_key = set(i for i, e in enumerate(key) if None not in e)
        idxs_val = set(i for i, e in enumerate(val) if None not in e)
        idxs = idxs_key & idxs_val # intersection
        idxs = sorted(list(idxs))
        key = tuple(key[i] for i in idxs)
        val = tuple(val[i] for i in idxs)
        return key, val

##__________________________________________________________________||
