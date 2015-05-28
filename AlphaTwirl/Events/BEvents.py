# Tai Sakuma <tai.sakuma@cern.ch>
from Branch import Branch
from Events import Events
from BranchAddressManager import BranchAddressManager
from BranchAddressManagerForVector import BranchAddressManagerForVector

##__________________________________________________________________||
branchAddressManager = BranchAddressManager()
branchAddressManagerForVector = BranchAddressManagerForVector()

##__________________________________________________________________||
class BEvents(Events):
    def __init__(self, tree, maxEvents = -1):
        super(BEvents, self).__init__(tree, maxEvents)
        tree.SetBranchStatus('*', 0)
        self.branches = { }

    def __getattr__(self, name):
        if name in self.branches: return self.branches[name]
        branch = self._buildBranch(self.tree, name)
        if branch is None: raise AttributeError("'" + str(self) + "' has no attribute '" + name + "'")
        self.branches[name] = branch
        if self.iEvent >= 0: self.tree.GetEntry(self.iEvent)
        return self.branches[name]

    def _buildBranch(self, tree, name):
        itsArray, itsCountArray = branchAddressManager.getArrays(tree, name)
        if itsArray is not None:
            branch = Branch(name, itsArray, itsCountArray)
            return branch
        itsVector = branchAddressManagerForVector.getVector(tree, name)
        if itsVector is not None:
            return itsVector # this can be used at a branch
        return None


##__________________________________________________________________||
