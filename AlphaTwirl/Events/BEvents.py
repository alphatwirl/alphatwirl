# Tai Sakuma <tai.sakuma@cern.ch>
from Events import Events
from BranchBuilder import BranchBuilder

##__________________________________________________________________||
class BEvents(Events):
    def __init__(self, tree, maxEvents = -1):
        super(BEvents, self).__init__(tree, maxEvents)
        tree.SetBranchStatus('*', 0)
        self.branches = { }
        self.buildBranch = BranchBuilder()

    def __getattr__(self, name):
        if name in self.branches: return self.branches[name]
        branch = self.buildBranch(self.tree, name)
        if branch is None: raise AttributeError("'" + str(self) + "' has no attribute '" + name + "'")
        self.branches[name] = branch
        if self.iEvent >= 0: self.tree.GetEntry(self.iEvent)
        return self.branches[name]

##__________________________________________________________________||
