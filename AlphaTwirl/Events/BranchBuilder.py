# Tai Sakuma <tai.sakuma@cern.ch>
from Branch import Branch
from BranchAddressManager import BranchAddressManager
from BranchAddressManagerForVector import BranchAddressManagerForVector

##__________________________________________________________________||
branchAddressManager = BranchAddressManager()
branchAddressManagerForVector = BranchAddressManagerForVector()

##__________________________________________________________________||
class BranchBuilder(object):
    """This class builds a branch.

    A branch is an object with data whose address is set in a tree.

    All instances of this class share the data.

    """

    itsdict = { }

    def __call__(self, tree, name):
        if (tree, name) in self.__class__.itsdict:
            return self.__class__.itsdict[(tree, name)]

        branch = self.imp(tree, name)
        self.__class__.itsdict[(tree, name)] = branch
        return branch

    def imp(self, tree, name):
        itsArray, itsCountArray = branchAddressManager.getArrays(tree, name)
        if itsArray is not None:
            branch = Branch(name, itsArray, itsCountArray)
            return branch
        itsVector = branchAddressManagerForVector.getVector(tree, name)
        if itsVector is not None:
            return itsVector # this can be used as a branch
        return None

##__________________________________________________________________||
