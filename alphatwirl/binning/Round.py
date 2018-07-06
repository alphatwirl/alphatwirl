# Tai Sakuma <tai.sakuma@gmail.com>

import math
import collections
import logging

from .ReturnTrue import ReturnTrue

##__________________________________________________________________||
class Round(object):
    def __init__(self, width=1, aboundary=None,
                 min=None, underflow_bin=None,
                 max=None, overflow_bin=None,
                 valid=ReturnTrue()):

        self.width = width
        self.aboundary = aboundary
        self.halfWidth = self.width/2 if self.width % 2 == 0 else float(self.width)/2
        if aboundary is None: aboundary = self.halfWidth
        self.boundaries = collections.deque([aboundary - width, aboundary, aboundary + width])
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
        return self._lower_boundary(val)

    def _lower_boundary(self, val):

        if not self.valid(val):
            return None

        if self.min is not None:
            if not self.min <= val:
                return self.underflow_bin

        if self.max is not None:
            if not val < self.max:
                return self.overflow_bin

        if math.isinf(val):
            logger = logging.getLogger(__name__)
            logger.warning('val={}. will return {}'.format(val, None))
            return None

        self._update_boundaries(val)

        bin = self.boundaries[0]
        for b in self.boundaries:
            if b <= val:
                bin = b
            else:
                break

        return bin

    def _update_boundaries(self, val):

        while val < self.boundaries[0]:
            self.boundaries.appendleft(self.boundaries[0] - self.width)

        while val > self.boundaries[-1]:
            self.boundaries.append(self.boundaries[-1] + self.width)

    def next(self, bin):
        return self._next_lower_boundary(bin)

    def _next_lower_boundary(self, bin):

        bin = self._lower_boundary(bin)

        if bin is None:
            return None

        if bin == self.underflow_bin:
            return self._lower_boundary(self.min)

        if bin == self.overflow_bin:
            return self.overflow_bin

        self._update_boundaries(bin)

        return self._lower_boundary(bin + self.width*1.001)

##__________________________________________________________________||
