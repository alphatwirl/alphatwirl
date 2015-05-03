# Tai Sakuma <tai.sakuma@cern.ch>
from Branch import Branch
from Events import Events
from BranchAddressManager import BranchAddressManager

##____________________________________________________________________________||
branchAddressManager = BranchAddressManager()

##____________________________________________________________________________||
class BEvents(Events):
    def __init__(self, tree, maxEvents = -1):
        super(BEvents, self).__init__(tree, maxEvents)
        tree.SetBranchStatus('*', 0)
        self.branches = { }

    def __getattr__(self, name):
        if name in self.branches: return self.branches[name]
        itsArray, itsCountArray = branchAddressManager.getArrays(self.tree, name)
        if itsArray is None: raise AttributeError("'" + str(self) + "' has no attribute '" + name + "'")
        self.branches[name] = Branch(name, itsArray, itsCountArray)
        if self.iEvent >= 0: self.tree.GetEntry(self.iEvent)
        return self.branches[name]

##____________________________________________________________________________||
