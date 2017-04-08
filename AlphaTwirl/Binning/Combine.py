# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
def plusOne(x): return x + 1

##__________________________________________________________________||
class Combine(object):
    """The Combine class allows one variable defined with two binnings to be
	combined into one list.  An instance of this class must be created with
	three arguments:
	``low`` -  the binning used below a specified threshold
	``high`` - the binning used above a specified threshold
	``at`` - the specified threshold (best as an integer if possible)

	an example instance of Combine is::

		low = Binning.Round(15.0, 50)
		high = Binning.RoundLog(0.1, 50)
		combBinning = Combine(low, high, at = 150)

	For example, consider studying jet pT with a linear scale for
	jet pT below 300, and a log scale for jet pT above 300.  The combination
	binning would be defined like this:

	lowpt = Round(45.0, 100)   #for 45.0 GeV wide bins
	highpt = RoundLog(0.1, 100)   #for variable bins which have a fixed 0.1 width in log scale
	ptbinning = Combine(low = lowpt, high = highpt, at = 300)

	where the last argument, at = 300, defines the point where the bins switch
	from linear to log scale.

	This class requires bin labels of both binnings to be values in
    the bins.

	The main function of this class is __call__.
	__call__ takes one input argument - the value of a variable or a bin.
	It returns the bin to which the input argument belongs.

	next takes one input argument - a bin.  It returns the bin immediately
	after the input bin.

	If an instance of the Combine class has already been created and is
	named obj, then __call__ and next are used as follows:

	obj.__call__(2)
	obj.next(3)

    """
    def __init__(self, low, high, at):
		"""initialize the two sets of bins, and the threshold 'at' where the
		binning switches from one set to the other set.

		"""
        self._low = low
        self._high = high
        self._at = at

    def __call__(self, val):
		"""return the bin to which val belongs.

		"""
        if val < self._at:
            return self._low(val)
        else:
            return self._high(val)

    def next(self, bin):
		"""first determine if the input bin argument belongs to the
		low set of bins below the threshold 'at', or the high set
		of bins used above the threshold 'at'.

		Then, use the next function already defined for the low or
		high set of bins to return the next bin.

		"""
        if bin < self._at:
            bin = self._low.next(bin)
            if bin < self._at:
                return bin
            else:
                return self._high(bin)
        return self._high.next(bin)

##__________________________________________________________________||
