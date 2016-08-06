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
        arrays = self._array_reader.read()

        # separate into keys and vals
        lenkey = len(self.keyAttrNames)
        keyvals = tuple((e[:lenkey], e[lenkey:]) for e in arrays)

        # apply binnings
        keyvals = tuple((tuple(b(k) for b, k in zip(self.binnings, kk)), vv) for kk, vv in keyvals)

        # remove None
        keyvals = tuple(e for e in keyvals if None not in e[0] and None not in e[1])

        return keyvals

##__________________________________________________________________||
