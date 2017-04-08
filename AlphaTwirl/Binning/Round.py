# Tai Sakuma <tai.sakuma@cern.ch>

import math
import collections
import logging

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class Round(object):
    """The Round class allows the user to define a set of fixed linear
	width bins used to summarize a variable.
	
	An instance of the Round class can be defined with several
	input arguments.  An instance can be created with no input args::

	roundBins = Round()

	A lower edge of one bin can be specified using ``aboundary``::

	roundBins = Round(aboundary = 10)

	A lower bin edge and bin width can be specified using ``width``
	and ``aboundary``::

	roundBins = Round(width = 5, aboundary = 10)

	If used, the lower bin edge specified by aboundary is the lowest
	value included in that particular bin.  The upper edge of every
	bin belongs to the next bin.

	If an instance of the Round class is made with no input args,
	or with ``width`` specified without ``aboundary``, then the
	bin boundaries will be set to half of ``width``.
	
	If the input variable is the leading jet pT in GeV, then
	the following binning would yield non-overlapping bins
	which are 20 GeV wide, and the lower edge of one bin would be
	100 GeV::
		
		jetptbin = Round(20, 100)

	One bin would cover 100 to 120 GeV, the next bin would cover
	120 to 140 GeV, the bin after that would cover 140 to 160 GeV,
	and so on.

	
	The main function of this class is __call__.  Given an input
	value or bin, the function returns the bin to which the input
	argument belongs.  Users must check that __call__ does not
	return None.  If an instance of the Round class named
	roundBins has been created, then __call__ is executed via::

	roundBins.__call__(2.5)

	this is equivalent to roundBins(2.5)

	A functor example of __call__ is::
    
	def test_call(self):
        obj = Round(2, 0)  #width is 2, aboundary is 0
        self.assertEqual( -2, obj( -1.9))
        self.assertEqual( -2, obj( -1  ))   #equivalent to calling obj.__call__(-1)
        self.assertEqual(  0, obj(  0.1))

	
	The next function takes a bin as an input argument, and
	returns the bin immediately following the input bin.  If
	the input bin is None, then None is returned.  If an
	instance of the Round class named roundBins has been
	created, then next is executed via::

	roundBins.next(4)

	A functor example of next is::
    
	def test_next(self):
        obj = Round(0.02, 0.005)   #width is 0.02, aboundary is 0.005
        self.assertEqual( -0.015, obj.next( -0.035))
        self.assertEqual(  0.005, obj.next( -0.015))
        self.assertEqual(  0.025, obj.next(  0.005))

    
	"""
    def __init__(self, width = 1, aboundary = None,
                 min = None, underflow_bin = None,
                 max = None, overflow_bin = None,
                 valid = returnTrue 
    ):
		"""__init__ creates an instance of the Round class.

		By default:
			every value added to the Round class object has the parameter
			valid set to True.  Thus, __call__ will never return None.
			specific max and min values are not set.
			specific underflow_bin and overflow_bin values are not set.

		underflow_bin could be set to -999, and overflow_bin could be
		set to the upper edge of the last bin.
		
		valid can be set to any user defined function which returns
		True or False.

		"""

        self.width = width
        self.aboundary = aboundary
        self.halfWidth = self.width/2 if self.width % 2 == 0 else float(self.width)/2
        if aboundary is None: aboundary = self.halfWidth
        self.boundaries = collections.deque([aboundary - width, aboundary, aboundary + width])
        #self.lowedge = (retvalue == 'lowedge')
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
		For improved performance the work done by this function has been moved
		to the function _lower_boundary, which is called automatically by
		__call__

		"""
        return self._lower_boundary(val)

	def _lower_boundary(self, val):
		"""returns the bin to which val belongs.
		This function is executed automatically by __call__, and should not be
		called explicitly by users.

		first check if the value val is valid.

		then, if min and max set in __init__ are not None, check if val belongs to the
		underflow (below min) or overflow bin (below max)

		then, check if val is plus or minus infinity. this is only necessary if max
		and/or min are not defined.

		This class keeps an internal list of bin boundaries named boundaries which is updated
		if a new value val is added which does not fall in an existing bin.
		
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

        self._update_boundaries(val)

        bin = self.boundaries[0]
        for b in self.boundaries:
            if b <= val:
                bin = b
            else:
                break

		return bin

    def _updateBoundaries(self, val):
		"""when a new value val is added that does not fit in an existing bin, this
		function creates a new bin in the internal list of bins.  This new bin has
		width equal to the class variable width.

		This function is called automatically when needed.  Users should not call
		this function explicitly.

		"""
        
		while val < self.boundaries[0]:
            self.boundaries.appendleft(self.boundaries[0] - self.width)

		while val > self.boundaries[-1]:
            self.boundaries.append(self.boundaries[-1] + self.width)

    def next(self, bin):
		"""given the input bin, this function returns the next bin.
		For improved performance the work done by this function has been moved
		to the function _next_lower_boundary, which is called automatically by
		next

		"""
        return self._next_lower_boundary(bin)

	def _next_lower_boundary(self, bin):
		"""given the input bin, this function returns the next bin.
		This function is automatically called by next, and should not be called
		explicitly by users.

		first check that the bin given in the argument bin exists in the set of bins already
		defined.  Return None if bin is not valid.

		if bin corresponds to underflow_bin, return the first bin (just above underflow_bin)
		
		if bin corresponds to overflow_bin, return the overflow_bin

		if bin is not None, and does not match underflow_bin or overflow_bin, then make
		sure that the bin already is saved in the internal list of bin boundaries named
		boundaries.  After this check, find the bin passed as input in the internal list
		of bin boundaries.  Return the next bin from the internal list of bin boundaries.

		"""

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
