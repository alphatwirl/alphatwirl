# Tai Sakuma <tai.sakuma@cern.ch>
from Branch import findBracnh

##____________________________________________________________________________||
class BEvents(object):
    def __init__(self, tree, maxEvents = -1):
        self.file = tree.GetDirectory() # so a file won't close
        self.tree = tree
        self.nEvents = min(self.tree.GetEntries(), maxEvents) if (maxEvents > -1) else self.tree.GetEntries()
        self.iEvent = -1
        tree.SetBranchStatus('*', 0)

        self.branches = { }

    def __iter__(self):
        for self.iEvent in xrange(self.nEvents):
            if self.tree.GetEntry(self.iEvent) <= 0: break
            yield self
        self.iEvent = -1

    def __getattr__(self, name):
        if name in self.branches: return self.branches[name]
        self.branches[name] = findBracnh(self.tree, name)
        return self.branches[name]

##____________________________________________________________________________||
