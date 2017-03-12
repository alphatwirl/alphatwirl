# Tai Sakuma <tai.sakuma@cern.ch>
from Round import Round
import math

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class RoundLog(object):
    """
	UPDATE THIS TO BE CONSISTENT WITH Round CLASS

	HOW TO INSTANTIATE

	if aBoundary is not given, then the bin boundaries are set to
	half the bin width

	EXECUTE __call__ AND DESCRIBE WHAT IS RETURNED

	EXECUTE __next__ AND DESCRIBE WHAT IS RETURNED
	
	SHOW FUNCTOR EXAMPLE see tests/unit/Binning/test_Round.py. Line 17
	is for call, and the object is defined on line 18.
	
	Similar to the Round class, the RoundLog class allows the user
	to define a set of bins used to summarize a variable that have a
	fixed width in log scale.  The actual widths of the bins are
	defined in log base 10.  The bin boundary, if given, must be given
	in linear scale.

	An instance of the RoundLog class is defined with two arguments.  The
	first specifies the width of every bin in log base 10 of the units used
	to make the TTree branch.  The second argument identifies one particular
	bin boundary - the upper edge of one bin, and the lower edge of
	the next bin.  The RoundLog class studies the input TTree branch and
	chooses the lower edge value of the lowest bin so that the user
	defined bin boundary and bin width are respected, there are no
	underflow events, and the number of initial bins (starting with
	bin number 1) with zero entries is minimized.  The RoundLog class
	will automatically create more bins until there are no overflow events.

	If an input TTree contains a branch with the leading jet pT in
	GeV, then the following binning would yield non-overlapping bins
	which are 0.1 units wide in log(GeV), and the lower edge of one
	bin would be 100 GeV::
		
		jetptlogbin = RoundLog(0.1, 100)

	One bin would cover 2.0 (100 GeV in log base 10) to 2.1 (125 GeV
	in log base 10), the next bin would cover 2.1 to 2.2 (158 GeV in
	log base 10), and so on.
	
	
    """
    def __init__(self, width = 0.1, aBoundary = 1,
                 min = None, underflow_bin = None,
                 max = None, overflow_bin = None,
                 valid = returnTrue,
                 retvalue = 'lowedge',
    ):
        self._round = Round(width = width, aBoundary = math.log10(aBoundary), retvalue = retvalue)
        self.width = width
        self.aBoundary = aBoundary
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

        val = math.log10(val)
        val = self._round(val)

        if val is None:
            return None

        return 10**val

    def next(self, bin):

        bin = self.__call__(bin)

        if bin is None:
            return None

        if bin == self.underflow_bin:
            return self.__call__(self.min)

        if bin == 0:
            return 0

        if bin == self.overflow_bin:
            return self.overflow_bin

        bin = math.log10(bin)
        return 10**self._round.next(bin)

##__________________________________________________________________||
