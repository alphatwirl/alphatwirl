# Tai Sakuma <tai.sakuma@cern.ch>

import math
import logging

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class Round(object):
    """The Round class allows the user to define a set of fixed linear
	width bins used to summarize a variable.  This can also be done with the
	Binning class, but using the Round class will yield more
	intelligently chosen bins (in terms of their lower and upper edges)
	in less time.

	An instance of the Round class is defined with two arguments.  The
	first specifies the width of every bin in the units used to make
	the TTree branch.  The second argument identifies one particular
	bin boundary - the upper edge of one bin, and the lower edge of
	the next bin.  The Round class studies the input TTree branch and
	chooses the lower edge value of the lowest bin so that the user
	defined bin boundary and bin width are respected, there are no
	underflow events, and the number of initial bins (starting with
	bin number 1) with zero entries is minimized.  The Round class
	will automatically create more bins until there are no overflow events.

	If an input TTree contains a branch with the leading jet pT in
	GeV, then the following binning would yield non-overlapping bins
	which are 20 GeV wide, and the lower edge of one bin would be
	100 GeV::
		
		Round = AlphaTwirl.Binning.Round
		jetptbin = Round(20, 100)

	One bin would cover 100 to 120 GeV, the next bin would cover
	120 to 140 GeV, the bin after that would cover 140 to 160 GeV,
	and so on.
	
	
    """
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
