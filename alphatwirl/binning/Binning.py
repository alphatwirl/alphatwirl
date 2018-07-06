# Tai Sakuma <tai.sakuma@gmail.com>

from .ReturnTrue import ReturnTrue

##__________________________________________________________________||
class Binning(object):
    def __init__(self, boundaries=None, lows=None, ups=None,
                 retvalue='lowedge', bins=None, underflow_bin=None, overflow_bin=None,
                 valid=ReturnTrue()):

        if boundaries is None:
            if lows is None or ups is None:
                raise ValueError("Only either boundaries or pairs of lows and ups need to be given!")
            if not tuple(lows[1:]) == tuple(ups[:-1]):
                raise ValueError("Boundaries cannot be determined from lows=" + str(lows) + " and ups=" + str(ups))
            self.boundaries = tuple(lows) + (ups[-1], )
            self.lows = tuple(lows)
            self.ups = tuple(ups)
        else:
            if lows is not None or ups is not None:
                raise ValueError("Only either boundaries or pairs of lows and ups need to be given!")
            if len(boundaries) < 2:
                raise ValueError("Needs at least one bin! boundaries=" + str(boundaries))
            self.boundaries = tuple(boundaries)
            self.lows = tuple(boundaries[:-1])
            self.ups = tuple(boundaries[1:])

        supportedRetvalues = ('number', 'lowedge')
        if retvalue not in supportedRetvalues:
            raise ValueError("The retvalue '%s' is not supported! " % (retvalue, ) + "Supported values are '" + "', '".join(supportedRetvalues)  + "'")

        self.lowedge = (retvalue == 'lowedge')
        if self.lowedge:
            if bins is not None: raise ValueError("bins cannot be given when retvalue is '" + retvalue + "'!")
            if underflow_bin is not None: raise ValueError("underflow_bin cannot be given when retvalue is '" + retvalue + "'!")
            if overflow_bin is not None: raise ValueError("overflow_bin cannot be given when retvalue is '" + retvalue + "'!")

        if self.lowedge:
            self.bins = self.lows
            self.underflow_bin = float("-inf")
            self.overflow_bin = self.ups[-1]
        else:
            self.bins = bins if bins is not None else tuple(range(1, len(self.lows) + 1))
            self.underflow_bin = underflow_bin if underflow_bin is not None else min(self.bins) - 1
            self.overflow_bin = overflow_bin if overflow_bin is not None else max(self.bins) + 1

        self._valid = valid

    def __repr__(self):
        return '{}(boundaries={!r}, underflow_bin={!r}, overflow_bin={!r}, valid={!r})'.format(
            self.__class__.__name__,
            self.boundaries, self.underflow_bin, self.overflow_bin, self._valid
        )

    def __call__(self, val):
        if not self._valid(val): return None
        if val < self.lows[0]: return self.underflow_bin
        if self.ups[-1] <= val: return self.overflow_bin
        return [b for b, l, u in zip(self.bins, self.lows, self.ups) if l <= val < u][0]

    def next(self, bin):
        if self.lowedge:
            # call self._call__() to ensure that the 'bin' is indeed one of the
            # bins.
            bin = self.__call__(bin)

        if bin == self.underflow_bin: return self.bins[0]
        if bin == self.overflow_bin: return self.overflow_bin
        if bin == self.bins[-1]: return self.overflow_bin
        return self.bins[self.bins.index(bin) + 1]

##__________________________________________________________________||
