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
        if not self._branch_exist(tree, name): return None

        branch = self._try_ctypes_or_array_of_ctypes(tree, name)
        if branch is not None: return branch

        branch = self._try_std_vector(tree, name)
        if branch is not None: return branch

        self._unknown_type_warning(tree, name)

        return None

    def _branch_exist(self, tree, name):
        leafNames = [l.GetName() for l in tree.GetListOfLeaves()]
        if name in leafNames: return True
        return False

    def _try_ctypes_or_array_of_ctypes(self, tree, name):
        itsArray, itsCountArray = branchAddressManager.getArrays(tree, name)
        if itsArray is None: return None
        branch = Branch(name, itsArray, itsCountArray)
        return branch

    def _try_std_vector(self, tree, name):
        itsVector = branchAddressManagerForVector.getVector(tree, name)
        return itsVector # this can be used as a branch

    def _unknown_type_warning(self, tree, name):
        import logging
        leaf = tree.GetLeaf(name)
        typename = leaf.GetTypeName()
        logging.warning("'" + self.__class__.__name__
            + "': unknown leaf type '" + typename + "'")

##__________________________________________________________________||
