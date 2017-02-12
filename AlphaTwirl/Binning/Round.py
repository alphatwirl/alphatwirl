# Tai Sakuma <tai.sakuma@cern.ch>

import math
import logging

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class Round(object):
    def __init__(self, width = 1, aBoundary = None,
                 min = None, underflow_bin = None,
                 max = None, overflow_bin = None,
                 valid = returnTrue, retvalue = 'lowedge'
    ):

        supportedRetvalues = ('center', 'lowedge')
        if retvalue not in supportedRetvalues:
            raise ValueError("The retvalue '%s' is not supported! " % (retvalue, ) + "Supported values are '" + "', '".join(supportedRetvalues)  + "'")

        self.width = width
        self.aBoundary = aBoundary
        self.halfWidth = self.width/2 if self.width % 2 == 0 else float(self.width)/2
        if aBoundary is None: aBoundary = self.halfWidth
        self.boundaries = [aBoundary - width, aBoundary, aBoundary + width]
        self.lowedge = (retvalue == 'lowedge')
        self.min = min
        self.underflow_bin = underflow_bin
        self.max = max
        self.overflow_bin = overflow_bin
        self.valid = valid

    def __repr__(self):
        return '{}(width = {!r}, aBoundary = {!r}, min = {!r}, underflow_bin = {!r}, max = {!r}, overflow_bin = {!r}, valid = {!r})'.format(
            self.__class__.__name__,
            self.width,
            self.aBoundary,
            self.min,
            self.underflow_bin,
            self.max,
            self.overflow_bin,
            self.valid
        )

    def __call__(self, val):

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
            logger.warning('val = {}. will return {}'.format(val, None))
            return None

        self._updateBoundaries(val)
        bin = self.boundaries[0]

        for b in self.boundaries[1:]:
            if b <= val: bin = b
            else: break

        if not self.lowedge:
            bin += self.halfWidth

        return bin

    def _updateBoundaries(self, val):
        while val < self.boundaries[0]:
            self.boundaries.insert(0, self.boundaries[0] - self.width)

        while val > self.boundaries[-1]:
            self.boundaries.append(self.boundaries[-1] + self.width)

    def next(self, bin):

        bin = self.__call__(bin)

        if bin is None:
            return None

        if bin == self.underflow_bin:
            return self.__call__(self.min)

        if bin == self.overflow_bin:
            return self.overflow_bin

        self._updateBoundaries(bin)
        self._updateBoundaries(bin + self.width)

        nbin = self.boundaries[0]

        for b in self.boundaries[1:]:
            if b <= bin: nbin = b
            else: break

        ret = self.boundaries[self.boundaries.index(nbin) + 1]

        if not self.lowedge:
            ret += self.halfWidth

        return ret

##__________________________________________________________________||
