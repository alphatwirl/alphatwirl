# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class GenericKeyComposer(object):
    """This class compose a key for the event.

    (this docstring is under development.)

    A key is a tuple of bins. The class returns a tuple of keys, i.e.,
    a tuple of tuples. Currently, the tuple has at most one element
    (one key).

    __init__ takes two mandatory arguments branchNames and binnings
    and one optional argument indices. These arguments are arrays or
    tuples with the same length.

    This class assumes a branch can be accessed as an attribute of the
    event, e.g., event.jet_pt.

    A branch can contain either a value or an array of values. If at
    least one of the branches contains an array, indices need to be
    given. The indices are a list of indices of arrays. An index for a
    branch that is not for an array should be None. For example, if
    indices are (0, None), the class assumes the first branch is an
    array and the second is a value. It then accesses the first
    element of the first branch and the value of the second branch.

    If the array is not long enough to contain the index specified,
    the class returns an empty tuple.


    The class uses the binnings to obtain bins for the values in the
    branches.

    """
    def __init__(self, branchNames, binnings, indices = None):
        self.branchNames = branchNames
        self.binnings = binnings
        self.indices = indices if indices is not None else [None]*len(self.branchNames)

    def begin(self, event): pass

    def __call__(self, event):
        ret = [ ]
        for varName, binning, index in zip(self.branchNames, self.binnings, self.indices):
            var = getattr(event, varName)
            if index is not None:
                if len(var) <= index: return ()
                var = var[index]
            var_bin = binning(var)
            if var_bin is None: return ()
            ret.append(var_bin)
        return (tuple(ret), )

##____________________________________________________________________________||
class GenericKeyComposerFactory(object):
    def __init__(self, branchNames, binnings, indices = None):
        self.branchNames = branchNames
        self.binnings = binnings
        self.indices = indices
    def __call__(self):
        return GenericKeyComposer(branchNames = self.branchNames, binnings = self.binnings, indices = self.indices)

##____________________________________________________________________________||
