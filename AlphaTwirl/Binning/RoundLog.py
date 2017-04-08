# Tai Sakuma <tai.sakuma@cern.ch>
from Round import Round
import math

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class RoundLog(object):
    """The RoundLog class allows the user to define a set of bins to
	summarize a variable with constant bin widths whose value is fixed
	in log base 10 scale.

	An instance of the RoundLog class can be created as follows::

	roundLogBins = RoundLog(0.1, 100)

	where 0.1 is the width (``width``) of each bin in log base 10, and the
	lower edge of one bin (``aboundary``) is 100.  In this
	example, one bin whose low edge is 100 would cover values
	between 2.0 (100) and 2.1 (125) in log base 10.  The next
	bin would cover 2.1 to 2.2 (158) in log base 10, and so on.  If
	a bin boundary is given, it must be given in linear scale.
	
	If an instance of the RoundLog class is made with no input args,
	or with ``width`` specified without ``aboundary``, then the
	bin boundaries will be set to half of ``width``.

	
	The main function of this class is __call__.  Given an input
	value or bin, the function returns the bin to which the input
	argument belongs.  Users must check that __call__ does not
	return None.  If an instance of the RoundLog class named
	roundLogBins has been created, then __call__ is executed via::

	roundLogBins.__call__(2.5)

	this is equivalent to roundLogBins(2.5)

	A functor example of __call__ is::
    
	def test_call(self):
        obj = RoundLog(0.1, 100)  #width is 0.1 in log scale, aboundary is 100
        self.assertEqual( 100, obj( 100))

	
	The next function takes a bin as an input argument, and
	returns the bin immediately following the input bin.  If
	the input bin is None, then None is returned.  If an
	instance of the RoundLog class named roundLogBins has been
	created, then next is executed via::

	roundLogBins.next(3)

	A functor example of next is::
    
	def test_next(self):
		obj = RoundLog(retvalue = 'center')  #the default bin width defined in __init__ is used
        self.assertAlmostEqual( 2.818382931264, obj.next(2.23872113856834))
        self.assertAlmostEqual( 28.18382931264, obj.next(22.3872113856834))




    """
    def __init__(self, width = 0.1, aboundary = 1,
                 min = None, underflow_bin = None,
                 max = None, overflow_bin = None,
                 valid = returnTrue,
                 retvalue = 'lowedge',
    ):
		"""valid can be any user defined function which returns True or False.
		retvalue can be lowedge or center.  See Round.py class for information
		about other __init__ input parameters.

		"""
        self._round = Round(width = width, aboundary = math.log10(aboundary), retvalue = retvalue)
        self.width = width
        self.aboundary = aboundary
        self.min = min
        self.underflow_bin = underflow_bin
        self.max = max
        self.overflow_bin = overflow_bin
        self.valid = valid

    def __repr__(self):
        return '{}(width = {!r}, aboundary = {!r}, min = {!r}, underflow_bin = {!r}, max = {!r}, overflow_bin = {!r}, valid = {!r})'.format(
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
		"""main function of this class. returns the bin to which val belongs.
		
		check if the input val is valid (return None if not valid), then
		check if the input val is zero, or falls in the underflow or
		overflow bin.  If none of these conditions are met, use the
		__call__ function defined in the Round class to determine the bin
		to which val belongs.

		"""

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
		"""given the input bin, this function returns the next bin.

		first check that the bin given in the argument 'bin' exists in the set of bins already
		defined.  Return None if bin is not valid.

		if bin corresponds to underflow_bin, return the first bin (just above underflow_bin)
		
		if bin corresponds to overflow_bin, return the overflow_bin

		if bin is not None, and does not match underflow_bin or overflow_bin, then use the
		next function defined in the Round class to identify the next bin.

		"""

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
