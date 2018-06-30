# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from .parse_indices_config import parse_indices_config
from .BackrefMultipleArrayReader import BackrefMultipleArrayReader

##__________________________________________________________________||
class KeyValueComposer(object):
    """This class composes keys and values for the event

    (this docstring is under development.)

    This class can be used with BEvents.

    This class supports inclusive indices '*'

    This class supports back references.


    """
    def __init__(self, keyAttrNames=None, binnings=None, keyIndices=None,
                 valAttrNames=None, valIndices=None):

        # for __repr__()
        name_value_pairs = (
            ('keyAttrNames', keyAttrNames),
            ('binnings', binnings),
            ('keyIndices', keyIndices),
            ('valAttrNames', valAttrNames),
            ('valIndices', valIndices),
        )
        self._repr = '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

        key_attr_names = tuple(keyAttrNames) if keyAttrNames is not None else ()
        key_idxs = tuple(keyIndices) if keyIndices is not None else (None, )*len(key_attr_names)
        val_attr_names = tuple(valAttrNames) if valAttrNames is not None else ()
        val_idxs = tuple(valIndices) if valIndices is not None else (None, )*len(val_attr_names)

        if not len(key_attr_names) == len(key_idxs):
            raise ValueError(
                "the two tuples must have the same length: key_attr_names={}, key_idxs={}".format(
                    key_attr_names, key_idxs
                )
            )

        if not len(val_attr_names) == len(val_idxs):
            raise ValueError(
                "the two tuples must have the same length: val_attr_names={}, val_idxs={}".format(
                    val_attr_names, val_idxs
                )
            )

        self.binnings = tuple(binnings) if binnings is not None else None
        if self.binnings is not None and not len(key_attr_names) == len(self.binnings):
            raise ValueError(
                "the two tuples must have the same length: key_attr_names={}, self.binnings={}".format(
                    key_attr_names, self.binnings
                )
            )

        self._lenkey = len(key_attr_names)
        self.attr_names = key_attr_names + val_attr_names
        self.idxs_conf = key_idxs + val_idxs
        self.backref_idxs, self.idxs_conf = parse_indices_config(self.idxs_conf)

        self.ArrayReader = BackrefMultipleArrayReader

    def __repr__(self):
        return self._repr

    def begin(self, event):
        arrays = self._collect_arrays(event, self.attr_names)
        self.active = True if arrays is not None else False
        if not self.active: return
        self._array_reader = self.ArrayReader(arrays, self.idxs_conf, self.backref_idxs)

    def _collect_arrays(self, event, attr_names):
        ret = [ ]
        for varname in attr_names:
            try:
                attr = getattr(event, varname)
            except AttributeError as e:
                logger = logging.getLogger(__name__)
                logger.warning('{!r}: {!s}'.format(self, e))
                return None
            ret.append(attr)
        return ret

    def __call__(self, event):
        if not self.active: return ()

        try:
            arrays = self._array_reader.read()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(e)
            logger.error(self)
            raise
        # e.g.,
        # arrays = (
        #     (1001, 15.3, -1.2, 20.2,  2.2, 0.1, 16.2, 22.1),
        #     (1001, 15.3, -1.2, 11.9,  1.2, 0.1, 16.2, 15.2),
        #     (1001, 15.3, -1.2, 13.3, -1.5, 0.1, 16.2, 16.3),
        #     (1001, 12.9,  5.2, 20.2,  2.2, 0.6, 13.1, 22.1),
        #     (1001, 12.9,  5.2, 11.9,  1.2, 0.6, 13.1, 15.2),
        #     (1001, 12.9,  5.2, 13.3, -1.5, 0.6, 13.1, 16.3),
        #     (1001,  9.2,  2.2, 20.2,  2.2, 1.2, 10.1, 22.1),
        #     (1001,  9.2,  2.2, 11.9,  1.2, 1.2, 10.1, 15.2),
        #     (1001,  9.2,  2.2, 13.3, -1.5, 1.2, 10.1, 16.3)
        # )


        # separate into keys and vals
        keyvals = tuple((e[:self._lenkey], e[self._lenkey:]) for e in arrays)
        # e.g.,
        # keyvals = (
        #     ((1001, 15.3, -1.2, 20.2,  2.2, 0.1), (16.2, 22.1)),
        #     ((1001, 15.3, -1.2, 11.9,  1.2, 0.1), (16.2, 15.2)),
        #     ((1001, 15.3, -1.2, 13.3, -1.5, 0.1), (16.2, 16.3)),
        #     ((1001, 12.9,  5.2, 20.2,  2.2, 0.6), (13.1, 22.1)),
        #     ((1001, 12.9,  5.2, 11.9,  1.2, 0.6), (13.1, 15.2)),
        #     ((1001, 12.9,  5.2, 13.3, -1.5, 0.6), (13.1, 16.3)),
        #     ((1001,  9.2,  2.2, 20.2,  2.2, 1.2), (10.1, 22.1)),
        #     ((1001,  9.2,  2.2, 11.9,  1.2, 1.2), (10.1, 15.2)),
        #     ((1001,  9.2,  2.2, 13.3, -1.5, 1.2), (10.1, 16.3))
        # )


        # apply binnings
        if self.binnings:
            keyvals = tuple((tuple(b(k) for b, k in zip(self.binnings, kk)), vv) for kk, vv in keyvals)
        # e.g.,
        # keyvals = (
        #     ((1001, 15,   -2, 20, None, 0.1), (16.2, 22.1)),
        #     ((1001, 15,   -2, 11,    1, 0.1), (16.2, 15.2)),
        #     ((1001, 15,   -2, 13,   -2, 0.1), (16.2, 16.3)),
        #     ((1001, 12, None, 20, None, 0.6), (13.1, 22.1)),
        #     ((1001, 12, None, 11,    1, 0.6), (13.1, 15.2)),
        #     ((1001, 12, None, 13,   -2, 0.6), (13.1, 16.3)),
        #     ((1001,  9,    2, 20, None, 1.2), (10.1, 22.1)),
        #     ((1001,  9,    2, 11,    1, 1.2), (10.1, 15.2)),
        #     ((1001,  9,    2, 13,   -2, 1.2), (10.1, 16.3))
        # )

        # remove None
        keyvals = tuple(e for e in keyvals if None not in e[0] and None not in e[1])
        # e.g.,
        # keyvals = (
        #     ((1001, 15, -2, 11,  1, 0.1), (16.2, 15.2)),
        #     ((1001, 15, -2, 13, -2, 0.1), (16.2, 16.3)),
        #     ((1001,  9,  2, 11,  1, 1.2), (10.1, 15.2)),
        #     ((1001,  9,  2, 13, -2, 1.2), (10.1, 16.3))
        # )

        return keyvals

##__________________________________________________________________||
