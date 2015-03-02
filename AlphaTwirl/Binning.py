# Tai Sakuma <sakuma@fnal.gov>
import decimal

##____________________________________________________________________________||
class Binning(object):
    def __init__(self, boundaries = None, lows = None, ups = None,
                 retvalue = 'number', bins = None, underflow_bin = None, overflow_bin = None):

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
class Round(object):
    def __init__(self, width = 1, aBoundary = None, retvalue = 'center'):
        self.width = decimal.Decimal(str(width))
        self.halfWidth = self.width/2

        # take Decimal after the modulo because the modulo on Decimals returns a
        # negetive number when aBoundary is negative
        self.aBoundary = self.halfWidth if aBoundary is None else decimal.Decimal(str(aBoundary % width))

        self.shift = self.halfWidth - self.aBoundary

        supportedRetvalues = ('center', 'lowedge')
        if retvalue not in supportedRetvalues:
            raise ValueError("The retvalue '%s' is not supported! " % (retvalue, ) + "Supported values are '" + "', '".join(supportedRetvalues)  + "'")

        self.lowedge = (retvalue == 'lowedge')

        self._context_ROUND_HALF_UP = decimal.Context(rounding = decimal.ROUND_HALF_UP)
        self._context_ROUND_HALF_DOWN = decimal.Context(rounding= decimal.ROUND_HALF_DOWN)

    def __call__(self, val):
        try:
            return [self.__call__(v) for v in val]
        except TypeError:
            pass
        return float(self._callImpDecimal(val))

    def _callImpDecimal(self, val):
        val = decimal.Decimal(str(val))
        ret = (val + self.shift)/self.width

        # the context ensures to include the lower edge in the bin
        context = self._context_ROUND_HALF_DOWN if val.is_signed() else self._context_ROUND_HALF_UP
        ret = ret.to_integral_value(context = context)

        ret = ret*self.width - self.shift
        if self.lowedge: ret = ret - self.halfWidth
        return ret

    def next(self, bin):
        try:
            return [self.next(v) for v in bin]
        except TypeError:
            pass

        # call self._callImpDecimal() to ensure that the 'bin' is indeed one of
        # the bins. As long as the retvalue is 'center' or 'lowedge', which are
        # all implemented at the moment, theBin will be the bin regardless of
        # whether the 'bin' is a value or a bin. This won't be true for the
        # retvalue 'upedge', which is not implemented, because the upedge
        # belongs to the next bin.
        theBin = self._callImpDecimal(bin)
        theNextBin = theBin + self.width
        return float(theNextBin)

##____________________________________________________________________________||
class Echo(object):
    def __call__(self, val):
        return val

##____________________________________________________________________________||
