#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class Binning(object):
    def __init__(self, boundaries = None, lows = None, ups = None, bins = None,
                 underflow_bin = None, overflow_bin = None):

        if boundaries is None:
            if lows is None or ups is None:
                raise ValueError("Only either boundaries or pairs of lows and ups need to be given!")
            if not tuple(lows[1:]) == tuple(ups[:-1]):
                raise ValueError("Boundaries cannot be determined from lows = " + str(lows) + " and ups = " + str(ups))
            self.boundaries = tuple(lows) + (ups[-1], )
            self.lows = tuple(lows)
            self.ups = tuple(ups)

        if boundaries is not None:
            if lows is not None or ups is not None:
                raise ValueError("Only either boundaries or pairs of lows and ups need to be given!")
            self.boundaries = tuple(boundaries)
            self.lows = tuple(boundaries[:-1])
            self.ups = tuple(boundaries[1:])

        self.bins = bins if bins is not None else tuple(range(1, len(self.lows) + 1))
        self.underflow_bin = underflow_bin if underflow_bin is not None else min(self.bins) - 1
        self.overflow_bin = overflow_bin if overflow_bin is not None else max(self.bins) + 1

    def __call__(self, val):
        try:
            return [self.__call__(v) for v in val]
        except TypeError:
            pass
        if val < self.lows[0]: return self.underflow_bin
        if self.ups[-1] <= val: return self.overflow_bin
        return [b for b, l, u in zip(self.bins, self.lows, self.ups) if l <= val < u][0]

    def __str__(self):
        ret = "%5s %10s %10s\n" % ("bin", "low", "up")
        return ret + "\n".join("%5s %10s %10s" % (str(b), str(l), str(u)) for b, l, u in zip(self.bins, self.lows, self.ups))

##____________________________________________________________________________||
