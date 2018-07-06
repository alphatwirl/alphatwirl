# Tai Sakuma <tai.sakuma@gmail.com>
import math

from .Round import Round
from .ReturnTrue import ReturnTrue

##__________________________________________________________________||
class RoundLog(object):
    def __init__(self, width=0.1, aboundary=1,
                 min=None, underflow_bin=None,
                 max=None, overflow_bin=None,
                 valid=ReturnTrue()):

        self._round = Round(width=width, aboundary=math.log10(aboundary))
        self.width = width
        self.aboundary = aboundary
        self.min = min
        self.underflow_bin = underflow_bin
        self.max = max
        self.overflow_bin = overflow_bin
        self.valid = valid

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

        if not self.valid(val):
            return None

        if val < 0:
            return None

        if val == 0:
            return 0

        if self.min is not None:
            if not self.min <= val:
                return self.underflow_bin

        if self.max is not None:
            if not val < self.max:
                return self.overflow_bin

        return val

    def next(self, bin):

        bin = self._valid_underflow_overflow(bin)

        if bin is None:
            return None

        if bin == self.underflow_bin:
            return self.__call__(self.min)

        if bin == 0:
            return 0

        if bin == self.overflow_bin:
            return self.overflow_bin

        bin = math.log10(bin)
        bin = self._round(bin)

        if bin is None:
            return None

        return 10**self._round.next(bin)

##__________________________________________________________________||
