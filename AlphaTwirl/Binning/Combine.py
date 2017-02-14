# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
def plusOne(x): return x + 1

##__________________________________________________________________||
class Combine(object):
    """The Combine class allows one variable defined with two binnings to be
	combined into one list.  An instance of this class must be created with
	three arguments: ``low``, the binning used below a specified
	threshold, ``high``, the binning used above a specified threshold, and
	``at``, the specified threshold (best as an int if possible)::

		low = Binning.Round(15.0, 50)
		high = Binning.RoundLog(0.1, 50)
		combBinning = Combine(low, high, at = 150)

	For example, consider studying jet pT with a linear scale for
	jet pT below 300, and a log scale for jet pT above 300. Only one entry in
	the main table defined in the AlphaTwirl executable file would be needed, and
	the binning in that executable would be defined like this:

	lowpt = Round(45.0, 100)   #for 45.0 GeV wide bins
	highpt = Round(0.1, 100)   #for variable bins which have a fixed 0.1 width in log scale
	ptbinning = Combine(low = lowpt, high = highpt, at = 300)

	where the last argument, at = 300, defines the point where the bins switch
	from linear to log scale.

	This class requires bin labels of both binnings to be values in
    the bins.

    """
    def __init__(self, low, high, at):
        self._low = low
        self._high = high
        self._at = at

    def __call__(self, val):
        if val < self._at:
            return self._low(val)
        else:
            return self._high(val)

    def next(self, bin):
        if bin < self._at:
            bin = self._low.next(bin)
            if bin < self._at:
                return bin
            else:
                return self._high(bin)
        return self._high.next(bin)

##__________________________________________________________________||
