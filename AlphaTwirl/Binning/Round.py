# Tai Sakuma <tai.sakuma@cern.ch>

import math
import logging

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class Round(object):
    """The Round class allows the user to define a set of fixed linear
	width bins used for an input variable.

	An instance of the Round class can be defined with several
	arguments.

	aBoundary is the lower edge of one particular bin.  The low edge
	belongs to the bin, whereas the upper edge of the bin belongs to
	the next bin.
	
	If the input variable is the leading jet pT in GeV, then
	the following binning would yield non-overlapping bins
	which are 20 GeV wide, and the lower edge of one bin would be
	100 GeV::
		
		jetptbin = Round(20, 100)

	One bin would cover 100 to 120 GeV, the next bin would cover
	120 to 140 GeV, the bin after that would cover 140 to 160 GeV,
	and so on.

	HOW TO INSTANTIATE

	if aBoundary is not given, then the bin boundaries are set to
	half the bin width

	EXECUTE __call__ AND DESCRIBE WHAT IS RETURNED

	EXECUTE __next__ AND DESCRIBE WHAT IS RETURNED
	
	SHOW FUNCTOR EXAMPLE see tests/unit/Binning/test_Round.py. Line 17
	is for call, and the object is defined on line 18.
	
	
    """
    def __init__(self, width = 1, aBoundary = None,
                 min = None, underflow_bin = None,
                 max = None, overflow_bin = None,
                 valid = returnTrue, retvalue = 'lowedge'
    ):
		"""similar to other binning classes, the argument 'valid' is a user defined function

		"""

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
		"""
		this function needs to be fast, as it is called many times when running
		the program.

		first check if the value 'val' added using __init__ is valid.

		then, if 'min' set in __init__ is not None, then check if 'val' belongs to the
		underflow (below 'min') or overflow bin (below max)

		then, check if 'val' is plus or minus infinity. this is only necessary if 'max'
		and/or 'min' is not defined.

		internally, this class keeps track of a list of bin boundaries.
		
		This list is named 'boundaries', and is updated
		if a new bin is needed in the internal list (either a new element at the
		beginning or end of the list).

		"""

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
		"""
		given a bin, this returns the next bin.

		first check that the bin given in the argument 'bin' exists in the set of bins already
		defined.  Return None if 'bin' is not valid.

		if bin corresponds to underflow_bin, return the first bin (just above underflow_bin)
		
		if bin corresponds to overflow_bin, return the overflow_bin

		if bin is not None, and does not match underflow_bin or overflow_bin, then make
		sure that the bin already is saved in the internal list of bin boundaries named
		'boundaries'

		then take the first bin boundary (lower edge of first bin just above underflow)
		and find and return the next bin.

		"""

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
