# Tai Sakuma <tai.sakuma@cern.ch>
from BranchAddressManager import BranchAddressManager

##____________________________________________________________________________||
class Branch(object):
    def __init__(self, name, array, countarray):
        self.name = name
        self.array = array
        self.countarray = countarray

    def __getitem__(self, i):
        if self.countarray is None and 0 != i:
            raise IndexError("the index should be zero for this branch: " + self.name + "[" + str(i) + "]")
        if self.countarray is not None and i >= self.countarray[0]:
            raise IndexError("the index is out of range: " + self.name + "[" + str(i) + "]")
        return self.array[i]

    def __len__(self):
        if self.countarray is None: return 1
        return self.countarray[0]

##____________________________________________________________________________||
branchAddressManager = BranchAddressManager()

##____________________________________________________________________________||
class BranchManager(object):
    def __init__(self):
        self.branches = { }

    def findBranch(self, tree, name):
        if name in self.branches: return self.branches[name]

        itsArray, itsCountArray = branchAddressManager.getArrays(tree, name)
        self.branches[name] = Branch(name, itsArray, itsCountArray)
        return self.branches[name]

##____________________________________________________________________________||
