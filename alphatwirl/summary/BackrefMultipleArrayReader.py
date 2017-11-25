# Tai Sakuma <tai.sakuma@cern.ch>
import itertools
import numbers

##__________________________________________________________________||
class BackrefMultipleArrayReader(object):
    def __init__(self, arrays, idxs_conf, backref_idxs = None):

        if not len(arrays) == len(idxs_conf):
            raise ValueError(
                "these two arguments must have the same length: arrays = {}, idxs_conf = {}".format(
                    arrays, idxs_conf
                )
            )

        if backref_idxs is not None:
            if not len(idxs_conf) == len(backref_idxs):
                raise ValueError(
                    "backref_idxs must have the same length as idxs_conf: idxs_conf = {}, backref_idxs = {}".format(
                        idxs_conf, backref_idxs
                    )
                )

        self.arrays = arrays
        self.wildcard_conf = tuple(c == '*' for c in idxs_conf)
        self.idxs_conf = tuple(c if isinstance(c, numbers.Number) else None for c in idxs_conf)

        if backref_idxs is None:
            self.use_backref = False
        else:
            self.use_backref = any([e is not None for e in backref_idxs])

        if not self.use_backref:
            self._zipped = list(zip(self.arrays, self.idxs_conf, self.wildcard_conf))
            return

        # use backref

        # e.g.
        # self.arrays = [[], [], [], [], [], [], [], []]
        # self.idxs_conf = (0, None, None, None, None, None, None, None)
        # self.wildcard_conf = (False, True, False, True, False, False, False, False)
        # backref_idxs = [None, None, 1, None, 3, 1, 1, 3]

        self.uniq_idxs = [ ]
        self.ref_idxs = [ ]
        for i in backref_idxs:
            if i is None:
                l = [ ]
                self.uniq_idxs.append(l)
                self.ref_idxs.append(l)
            else:
                self.ref_idxs.append(self.ref_idxs[i])

        # e.g.,
        # self.uniq_idxs = [[], [], []]
        # [id(o) for o in self.uniq_idxs] = [4738625048, 4738625480, 4738625120]
        # self.ref_idxs = [[], [], [], [], [], [], [], []]
        # [id(o) for o in self.ref_idxs] = [4738625048, 4738625480, 4738625480, 4738625120, 4738625120, 4738625480, 4738625480, 4738625120]

        self._zipped_1 = list(zip(self.arrays, self.idxs_conf, self.wildcard_conf, self.ref_idxs))
        self._zipped_2 = list(zip(self.arrays, self.ref_idxs))

    def read(self):
        if self.use_backref:
            return self._read_with_backref()
        return self._fast_read_without_backref()

    def _fast_read_without_backref(self):

        # e.g.,
        # self.idxs_conf = (1, None, None, 2, None)
        # self.wildcard_conf = (False, True, True, False, True)
        # self.arrays = [
        #     [55, 66, 77],
        #     [12, 13, 14],
        #     [104, 105],
        #     [222, 333, 444, 555],
        #     [1001, 1002, 1003]
        # ]

        # read arrays
        vals = [ ]
        for array, idx, wild in self._zipped:
            if wild:
                vals.append(list(array))
                continue
            if idx < len(array):
                vals.append([array[idx]])
                continue
            # idx is out of the range
            vals.append([ ])
        # e.g.,
        # vals = [
        #     [66],
        #     [12, 13, 14],
        #     [104, 105],
        #     [444],
        #     [1001, 1002, 1003]
        # ]

        # expand with all combinations
        ret =  tuple(itertools.product(*vals))
        # e.g.,
        # ret = (
        #     (66, 12, 104, 444, 1001),
        #     (66, 12, 104, 444, 1002),
        #     (66, 12, 104, 444, 1003),
        #     (66, 12, 105, 444, 1001),
        #     (66, 12, 105, 444, 1002),
        #     (66, 12, 105, 444, 1003),
        #     (66, 13, 104, 444, 1001),
        #     (66, 13, 104, 444, 1002),
        #     (66, 13, 104, 444, 1003),
        #     (66, 13, 105, 444, 1001),
        #     (66, 13, 105, 444, 1002),
        #     (66, 13, 105, 444, 1003),
        #     (66, 14, 104, 444, 1001),
        #     (66, 14, 104, 444, 1002),
        #     (66, 14, 104, 444, 1003),
        #     (66, 14, 105, 444, 1001),
        #     (66, 14, 105, 444, 1002),
        #     (66, 14, 105, 444, 1003)
        # )

        return ret

    def _read_with_backref(self):

        # e.g.,
        # self.arrays = [
        #     [1001],
        #     [12, 13, 14, 15],
        #     [104, 105, 106, 107],
        #     [51, 52],
        #     [84, 85, 86],
        #     [403, 404, 405],
        #     [207, 208, 209, 210],
        #     [91, 92, 93]
        # ]

        # initialize self.uniq_idxs
        for i in self.uniq_idxs:
            i[:] = [ ]
        # e.g.,
        # self.uniq_idxs = [[], [], []]
        # self.ref_idxs = [[], [], [], [], [], [], [], []]


        # fill self.ref_idxs
        for array, idx, wild, ref in self._zipped_1:
            larray = len(array)
            if idx is not None:
                ref[:] = [idx] if idx < larray else [ ]
                continue
            if wild:
                ref[:] = range(larray)
                continue
            # backref
            ref[:] = [j for j in ref if j < larray]
        # e.g.,
        # self.uniq_idxs = [
        #     [0],
        #     [0, 1, 2],
        #     [0, 1]
        # ]
        # self.ref_idxs = [
        #     [0],
        #     [0, 1, 2],
        #     [0, 1, 2],
        #     [0, 1],
        #     [0, 1],
        #     [0, 1, 2],
        #     [0, 1, 2],
        #     [0, 1]
        # ]

        # expand self.uniq_idxs with all combinations
        prod = tuple(itertools.product(*self.uniq_idxs))
        for i in range(len(self.uniq_idxs)):
            self.uniq_idxs[i][:] = [p[i] for p in prod]
        # e.g.,
        # self.uniq_idxs = [
        #     [0, 0, 0, 0, 0, 0],
        #     [0, 0, 1, 1, 2, 2],
        #     [0, 1, 0, 1, 0, 1]
        # ]
        # self.ref_idxs = [
        #     [0, 0, 0, 0, 0, 0],
        #     [0, 0, 1, 1, 2, 2],
        #     [0, 0, 1, 1, 2, 2],
        #     [0, 1, 0, 1, 0, 1],
        #     [0, 1, 0, 1, 0, 1],
        #     [0, 0, 1, 1, 2, 2],
        #     [0, 0, 1, 1, 2, 2],
        #     [0, 1, 0, 1, 0, 1]
        # ]

        ret = [[a[j] for j in i] for a, i in self._zipped_2]
        # e.g.,
        # ret = [
        #     [1001, 1001, 1001, 1001, 1001, 1001],
        #     [12, 12, 13, 13, 14, 14],
        #     [104, 104, 105, 105, 106, 106],
        #     [51, 52, 51, 52, 51, 52],
        #     [84, 85, 84, 85, 84, 85],
        #     [403, 403, 404, 404, 405, 405],
        #     [207, 207, 208, 208, 209, 209],
        #     [91, 92, 91, 92, 91, 92]
        # ]

        # take transpose
        ret = tuple(map(tuple, zip(*ret)))
        # e.g.,
        # ret = (
        #     (1001, 12, 104, 51, 84, 403, 207, 91),
        #     (1001, 12, 104, 52, 85, 403, 207, 92),
        #     (1001, 13, 105, 51, 84, 404, 208, 91),
        #     (1001, 13, 105, 52, 85, 404, 208, 92),
        #     (1001, 14, 106, 51, 84, 405, 209, 91),
        #     (1001, 14, 106, 52, 85, 405, 209, 92)
        # )
        return ret

##__________________________________________________________________||
