# Tai Sakuma <sakuma@fnal.gov>
import decimal

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
