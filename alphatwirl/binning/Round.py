# Tai Sakuma <tai.sakuma@gmail.com>

import math
import collections
import logging

from .search import binary_search

##__________________________________________________________________||
class Round(object):
    """Equal width binning

    Parameters
    ----------
    width : float or int, default 1
        The width.
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
    def __init__(self, width=1, aboundary=None,
                 min=None, underflow_bin=None,
                 max=None, overflow_bin=None,
                 valid=None):

        self.width = width
        self.aboundary = aboundary
        if aboundary is None:
            halfWidth = self.width//2 if self.width % 2 == 0 else float(self.width)/2
            aboundary = halfWidth
        self.boundaries = collections.deque([aboundary])
        self.min = min
        self.underflow_bin = underflow_bin
        self.max = max
        self.overflow_bin = overflow_bin
        self.valid = valid

        if self.min is not None:
            self._update_boundaries(self.min)

        if self.max is not None:
            self._update_boundaries(self.max)
            if self.overflow_bin is True:
                self.overflow_bin = self.boundaries[-1]

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

        if val is None:
            return None

        if self.valid:
            if not self.valid(val):
                return None

        if self.min is not None:
            if not self.boundaries[0] <= val:
                return self.underflow_bin

        if self.max is not None:
            if not val < self.boundaries[-1]:
                return self.overflow_bin

        if math.isinf(val):
            logger = logging.getLogger(__name__)
            logger.warning('val={}. will return {}'.format(val, None))
            return None

        self._update_boundaries(val)

        idx = binary_search(val, self.boundaries)
        return self.boundaries[idx]


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
