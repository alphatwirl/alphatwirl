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

	If a binning structure already exists in the input data (for example, with the number
	of jets or leptons in the event), then Echo can be used.  Alternatively,
	if the input has already been organized into categories with unique
	labels (string titles for example), then Echo can be used.

	An instance of the Echo class can be created as follows::

	newbins = Echo()

	The main function of this class is __call__.  __call__
	requires one input parameter which is a value of the
	variable being summarized.  It returns the bin to which
	the input value belongs.  Users must check that the
	return value is not None.

	The function next requires one input argument - a bin.
	Next returns the bin immediately after the input bin.

	If an instance of the Echo class named obj has already
	been defined, __call__ and next can be used as follows::

	obj.__call__(4)
	obj.next(3)
	
    """
    def __init__(self, nextFunc = plusOne, valid = returnTrue):
		"""nextFunc can be any user defined function.
		If the bins are identified with strings, then nextFunc can be
		set to None.

		if the input argument valid is not changed from returnTrue,
		then __call__ will never return None.

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
		"""main function of this class.  Given the input
		value val, this function returns the bin to which
		val belongs.  None is returned if the input val is
		not valid.
		
		"""
        if not self._valid(val): return None
        return val

    def next(self, bin):
		"""given the input bin, this function returns the
		bin immediately following the input bin argument.

		"""
        if self._nextFunc is None: return None
        return self._nextFunc(bin)

##__________________________________________________________________||
