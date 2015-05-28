# Tai Sakuma <tai.sakuma@cern.ch>
from Branch import Branch
from BranchAddressManager import BranchAddressManager
from BranchAddressManagerForVector import BranchAddressManagerForVector

##__________________________________________________________________||
branchAddressManager = BranchAddressManager()
branchAddressManagerForVector = BranchAddressManagerForVector()

##__________________________________________________________________||
class BranchBuilder(object):
    def __call__(self, tree, name):
        itsArray, itsCountArray = branchAddressManager.getArrays(tree, name)
        if itsArray is not None:
            branch = Branch(name, itsArray, itsCountArray)
            return branch
        itsVector = branchAddressManagerForVector.getVector(tree, name)
        if itsVector is not None:
            return itsVector # this can be used as a branch
        return None

##__________________________________________________________________||
