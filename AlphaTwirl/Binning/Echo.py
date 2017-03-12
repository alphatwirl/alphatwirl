# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
def plusOne(x): return x + 1

##__________________________________________________________________||
class Echo(object):
    """The Echo class is the simplest style of binning used in AlphaTwirl,
	and uses inputs which have already been sorted into bins (like nJets) or
	categories (strings).

	If a binning structure already exists (for example, with the number
	of jets or leptons in the event), then Echo can be used.  Alternatively,
	if the input has already been organized into categories with unique
	labels (string titles for example), then Echo can be used.

	HOW TO INSTANTIATE

	EXECUTE __call__ AND DESCRIBE WHAT IS RETURNED

	EXECUTE __next__ AND DESCRIBE WHAT IS RETURNED
	
    """
    def __init__(self, nextFunc = plusOne, valid = returnTrue):
		"""nextFunc can be any user defined function
		
		if the bins are identified with strings, then nextFunc can be
		set to None

		"""
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
		"""this will 

		"""
        if self._nextFunc is None: return None
        return self._nextFunc(bin)

##__________________________________________________________________||
