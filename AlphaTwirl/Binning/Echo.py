# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
def plusOne(x): return x + 1

##__________________________________________________________________||
class Echo(object):
    """The Echo class is the simplest style of binning used in AlphaTwirl,
	and works with any branch of an input TTree.
	
	AlphaTwirl takes TTrees as inputs, and with ROOT alone one could make
	a histogram from one branch of an input TTree without specifying a
	precise binning (in terms of the number of bins, lower bound and
	upper bound).  The default ROOT binning used to make a histogram from
	a TTree branch uses a lower bound which is low enough such that there are
	few or no underflow events, and an upper bound which is high enough
	such that there are few or no overflow events.  This default binning
	is used when AlphaTwirl is configured to read from one or more TTree branches
	and summarize the results with Echo binning, like in this example::

	tblcfg = [
		dict(outFileName = 'tbl_njets_nlepts.txt',
			branchNames = ('nJet50', 'nLept50'),
			outColumnNames = ('njets','nleptons'),
			binnings = (Echo(), Echo()),
			countsClass = Counts),
	]

	Echo binning is best used for quick tests of AlphaTwirl to see
	if something will work, and for TTree branches which store
	integer values, like the number of jets or leptons in the event.
	
    """
    def __init__(self, nextFunc = plusOne, valid = returnTrue):
        self._nextFunc = nextFunc
        self._valid = valid

    def __repr__(self):
        return '{}(nextFunc = {!r}, valid = {!r})'.format(
            self.__class__.__name__,
            self._nextFunc,
            self._valid
        )

    def __call__(self, val):
        if not self._valid(val): return None
        return val

    def next(self, bin):
        if self._nextFunc is None: return None
        return self._nextFunc(bin)

##__________________________________________________________________||
