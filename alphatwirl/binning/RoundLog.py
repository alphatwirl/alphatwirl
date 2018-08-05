# Tai Sakuma <tai.sakuma@gmail.com>
import math

from .Round import Round

##__________________________________________________________________||
class RoundLog(object):
    """Binning with equal width in log scale

    Parameters
    ----------
    width : float or int, default 1
        The common logarithm (log10) of the width.
    aboundary : float or int, optional
        A boundary. If not given, ``width/2`` will be used.
    min : float or int, optional
        The lowest bin will be the bin that ``min`` falls in. If given,
        ``__call__(val)`` returns ``underflow_bin`` if the ``val`` is less than
        the lower edge of the lowest bin.
    underflow_bin : optional
        The underflow bin. When ``min`` is given, the ``__call__(val)`` returns
        ``underflow_bin`` if the ``val`` is less than the lower edge of the
        lowest bin.
    max : float or int, optional
        The highest bin will be the bin that ``max`` falls in except when
        ``max`` is one of boundaries. When ``max`` is one of boundaries, the
        highest bin is the bin whose upper edge is ``max``. If given,
        ``__call__(val)`` returns the overflow bin if the ``val`` is greater
        than or equal to the upper edge of the highest bin.
    overflow_bin : optional
        The overflow bin if ``overflow_bin`` is any value other than ``True``.
        If ``overflow_bin`` is ``True``, the overflow bin will be the upper
        edge of the highest bin. When ``max`` is given, the ``__call__(val)``
        returns the overflow bin if the ``val`` is greater than or equal to the
        upper edge of the highest bin.
    valid : function, optional
        Boolean function to test if value is valid

    """
    def __init__(self, width=0.1, aboundary=1,
                 min=None, underflow_bin=None,
                 max=None, overflow_bin=None,
                 valid=None):

        self._round = Round(width=width, aboundary=math.log10(aboundary))
        self.width = width
        self.aboundary = aboundary
        self.min = min
        self.underflow_bin = underflow_bin
        self.max = max
        self.overflow_bin = overflow_bin
        self.valid = valid

        if self.min is None:
            self.min_bin_log10_lowedge = None
        else:
            self.min_bin_log10_lowedge = self._round(math.log10(self.min))

        if self.max is None:
            self.max_bin_log10_upedge = None
        else:
            self._round(math.log10(self.max)) # = self._round.boundaries[-2]
            self.max_bin_log10_upedge = self._round.boundaries[-1]
            if self.overflow_bin is True:
                self.overflow_bin = 10**self.max_bin_log10_upedge

    def __repr__(self):
        return '{}(width={!r}, aboundary={!r}, min={!r}, underflow_bin={!r}, max={!r}, overflow_bin={!r}, valid={!r})'.format(
            self.__class__.__name__,
            self.width,
            self.aboundary,
            self.min,
            self.underflow_bin,
            self.max,
            self.overflow_bin,
            self.valid
        )

    def __call__(self, val):

        val = self._valid_underflow_overflow(val)

        if val in (None, 0, self.underflow_bin, self.overflow_bin):
            return val

        val = math.log10(val)
        val = self._round(val)

        if val is None:
            return None

        return 10**val

    def _valid_underflow_overflow(self, val):

        if self.valid:
            if not self.valid(val):
                return None

        if val < 0:
            return None

        if val == 0:
            return 0

        if self.min_bin_log10_lowedge:
            if not self.min_bin_log10_lowedge <= math.log10(val):
                return self.underflow_bin

        if self.max_bin_log10_upedge:
            if not math.log10(val) < self.max_bin_log10_upedge:
                return self.overflow_bin

        return val

    def next(self, bin):

        if bin is None:
            return None

        if bin == self.underflow_bin:
            return self.__call__(self.min)

        if bin < 0:
            return None

        if bin == 0:
            return 0

        if bin == self.overflow_bin:
            return self.overflow_bin

        log10_bin = self._round(math.log10(bin))

        if log10_bin is None:
            return None

        log10_next = self._round.next(log10_bin)

        if self.max_bin_log10_upedge:
            if log10_next == self.max_bin_log10_upedge:
                return self.overflow_bin

        return 10**log10_next

##__________________________________________________________________||
