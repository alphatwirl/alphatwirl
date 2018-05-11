# Tai Sakuma <tai.sakuma@gmail.com>

import ROOT

from ..roottree.Events import Events

from .load_delphes import load_delphes

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
class TTreeWrap(object):
    """wrap ExRootTreeReader so that Events can treat it as TTree
    """
    def __init__(self, treeReader):
        self.treeReader = treeReader

    def GetEntries(self):
        return self.treeReader.GetEntries()

    def GetEntry(self, entry):
        return self.treeReader.ReadEntry(entry)

##__________________________________________________________________||
@_deprecated(msg='alphatwirl.delphes has been moved to https://github.com/alphatwirl/atdelphes.')
class DelphesEvents(Events):
    def __init__(self, tree, maxEvents = -1, start = 0):
        load_delphes()
        self.treeReader = ROOT.ExRootTreeReader(tree)
        super(DelphesEvents, self).__init__(
            tree = TTreeWrap(self.treeReader),
            maxEvents = maxEvents, start = start
        )
        self.branches = { }

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            super(DelphesEvents, self)._repr_contents()
        )

    def __getattr__(self, name):

        if name in self.branches:
            return self.branches[name]

        branch = self.treeReader.UseBranch(name)

        # branch = TClonesArrayWrap(branch) # can uncomment when TClonesArrayWrap works fast
        self.branches[name] = branch

        if self.iEvent >= 0:
            self.tree.GetEntry(self.start + self.iEvent)

        return self.branches[name]

##__________________________________________________________________||
