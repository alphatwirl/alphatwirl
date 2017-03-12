# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class Binning(object):
    """This is an abstract class which can run in any environment.  It
	doesn't know about ROOT TTrees or other ROOT things.  .
	
	The Binning class allows the set of bins used to summarize the
	information from one TTree branch to be defined with specific lower
	and upper bin edge values set by the user.
	
	An instance of the Binning class can be defined with a single argument
	``boundaries``, which is set equal to a list of the bin boundaries
	which start at the lowest value, and increase for every bin
	added, like::
		
		metbin = Binning(boundaries = (0, 100, 200, 400, 700, 1100))
	
	Alternatively, an instance of the Binning class can be defined with
	two arguments ``lows`` and ``ups``.  These two arguments are set equal
	to two lists of the same length that specify the lower and upper edge
	of every bin, like::
		
		jetPtBin = Binning(lows = (0, 20, 40, 60), ups = (20, 40, 60, 200))
	
	In general, if the results should be summarized in non-overlapping
	bins which completely cover a well defined domain of a variable, the
	single argument ``boundaries`` definition of the Binning class should
	be used.

	Two powerful features of the two argument definition of a Binning
	class instance are that a subset of variable values can be blinded
	from the summary created by AlphaTwirl, and overlapping bins can
	be defined.  If an input TTree passed to AlphaTwirl contains a branch
	with the dilepton mass using the two leading leptons in each event,
	the following binning would summarize events in 4 different bins
	that are all centered at 90 GeV::

		massOverlapBins = Binning(lows = (60, 70, 80, 85), ups = (120, 110, 100, 95))

	REMOVE OVERLAPPING BIN DISCUSSION.  It is not possible

	Using the same input TTree and dilepton mass branch, events with 
	dilepton mass between 85 and 95 would be ignored in the AlphaTwirl
	summary if the following binning is used::

		massIgnoreBins = Binning(lows = (70, 80, 95, 95), ups = (85, 85, 100, 110))

	HOW TO INSTANTIATE

	EXECUTE __call__ AND DESCRIBE WHAT IS RETURNED

	EXECUTE __next__ AND DESCRIBE WHAT IS RETURNED
	
	SHOW FUNCTOR EXAMPLE see tests/unit/Binning/test_Round.py. Line 17
	is for call, and the object is defined on line 18.
	

	
    """
    def __init__(self, boundaries = None, lows = None, ups = None,
                 retvalue = 'lowedge', bins = None, underflow_bin = None, overflow_bin = None,
                 valid = returnTrue):
		"""retvalue is automatically set to lowedge

		validity of added value is, by default 'returnTrue', always true
		if users want to check that the added value is actually valid, then they should
		change this default in __init__

		users can set specific values for the underflow_bin and overflow_bin, by
		default they are none.  an example for underflow_bin could be -999

		an example overflow_bin could be the upper edge of the last bin
		
		"""

        if boundaries is None:
            if lows is None or ups is None:
                raise ValueError("Only a list of bin boundaries, or pairs of (bin lower bound, bin upper bound) need to be given!")
            if not tuple(lows[1:]) == tuple(ups[:-1]):
                raise ValueError("Boundaries cannot be determined from lows = " + str(lows) + " and ups = " + str(ups))
            self.boundaries = tuple(lows) + (ups[-1], )
            self.lows = tuple(lows)
            self.ups = tuple(ups)
        else:
            if lows is not None or ups is not None:
                raise ValueError("Only either boundaries or pairs of lows and ups need to be given!")
            if len(boundaries) < 2:
                raise ValueError("Needs at least one bin! boundaries = " + str(boundaries))
            self.boundaries = tuple(boundaries)
            self.lows = tuple(boundaries[:-1])
            self.ups = tuple(boundaries[1:])

        supportedRetvalues = ('number', 'lowedge')
        if retvalue not in supportedRetvalues:
            raise ValueError("The retvalue '%s' is not supported! " % (retvalue, ) + "Supported values are '" + "', '".join(supportedRetvalues)  + "'")

        self.lowedge = (retvalue == 'lowedge')
        if self.lowedge:
            if bins is not None: raise ValueError("bins cannot be given when retvalue is '" + retvalue + "'!")
            if underflow_bin is not None: raise ValueError("underflow_bin cannot be given when retvalue is '" + retvalue + "'!")
            if overflow_bin is not None: raise ValueError("overflow_bin cannot be given when retvalue is '" + retvalue + "'!")

        if self.lowedge:
            self.bins = self.lows
            self.underflow_bin = float("-inf")
            self.overflow_bin = self.ups[-1]
        else:
            self.bins = bins if bins is not None else tuple(range(1, len(self.lows) + 1))
            self.underflow_bin = underflow_bin if underflow_bin is not None else min(self.bins) - 1
            self.overflow_bin = overflow_bin if overflow_bin is not None else max(self.bins) + 1

        self._valid = valid

    def __repr__(self):
        return '{}(boundaries = {!r}, underflow_bin = {!r}), overflow_bin = {!r}), valid = {!r})'.format(
            self.__class__.__name__,
            self.boundaries, self.underflow_bin, self.overflow_bin, self._valid
        )

    def __str__(self):
        ret = '{:>5} {:>10} {:>10}\n'.format('bin', 'low', 'up')
        return ret + "\n".join('{:>5} {:>10} {:>10}'.format(b, l, u) for b, l, u in zip(self.bins, self.lows, self.ups))

    def __call__(self, val):
		"""this is the main function of this class
		
		after class is instantiated, this class simply

		if val is not valid, null is returned.  By default, true is always returned if
		__init__ is modified such that the validity of the added value is changed from returnTrue
		
		USERS OF THIS BINNING CLASS must check that return value of __call__ is not None
		For example, if all values must be integers and a floating point number is
		given, then None is returned

		the upper boundary defined with __init__ belongs to the next bin, not the current
		bin.  Thus, the line which decides if a value belongs to overflow_bin uses greater
		than or equal to, not just greater than.

		in the return function, if the value 'val' is equal to the lower edge, then 'val'
		belongs to the current bin.
		
		"""
        if not self._valid(val): return None
        if val < self.lows[0]: return self.underflow_bin
        if self.ups[-1] <= val: return self.overflow_bin
        return [b for b, l, u in zip(self.bins, self.lows, self.ups) if l <= val < u][0]

    def next(self, bin):
		"""if you give one bin, this method returns the next bin
		
		in original implementation, the bins were just numbered, and
		the lower edge of each bin was tracked separately

		__call__ is called first to determine the correct current bin (this is tricky
		for bins whose edges are floating point values)
		
		if bin corresponds to underflow bin, then this function returns the lowest
		bin (just above underflow bin)

		if bin corresponds to overflow bin, then this function returns the overflow
		bin

		if bin corresponds to the last bin, then this function returns the overflow
		bin

		"""
        if self.lowedge:
            # call self._call__() to ensure that the 'bin' is indeed one of the
            # bins.
            bin = self.__call__(bin)

        if bin == self.underflow_bin: return self.bins[0]
        if bin == self.overflow_bin: return self.overflow_bin
        if bin == self.bins[-1]: return self.overflow_bin
        return self.bins[self.bins.index(bin) + 1]

##__________________________________________________________________||
