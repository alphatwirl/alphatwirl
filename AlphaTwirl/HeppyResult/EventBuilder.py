# Tai Sakuma <tai.sakuma@cern.ch>
import os
import ROOT
from ..Events import Events
from ..Events import EventsWithBranchAddressAccess

##____________________________________________________________________________||
class EventBuilder(object):
    def __init__(self, analyzerName, fileName, treeName, maxEvents = -1,
                 brancheNames = None, branchAddressAccess = False):
        self._analyzerName = analyzerName
        self._fileName = fileName
        self._treeName = treeName
        self._maxEvents = maxEvents
        self._brancheNames = brancheNames
        self._branchAddressAccess = branchAddressAccess

    def build(self, component):
        inputPath = os.path.join(getattr(component, self._analyzerName).path, self._fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self._treeName)
        if self._brancheNames is not None: self._disableAllUnnecessaryBranches(tree)
        if not self._branchAddressAccess:
            return Events(tree, self._maxEvents)
        else:
            return EventsWithBranchAddressAccess(tree, self._brancheNames, self._maxEvents)

    def _disableAllUnnecessaryBranches(self, tree):
        tree.SetBranchStatus('*', 0)
        for b in self._brancheNames:
            tree.SetBranchStatus(b, 1)

##____________________________________________________________________________||
