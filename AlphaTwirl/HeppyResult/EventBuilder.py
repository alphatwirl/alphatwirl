# Tai Sakuma <tai.sakuma@cern.ch>
import os
import ROOT
from ..Events import Events

##____________________________________________________________________________||
class EventBuilder(object):
    def __init__(self, analyzerName, fileName, treeName, maxEvents = -1, brancheNames = None):
        self._analyzerName = analyzerName
        self._fileName = fileName
        self._treeName = treeName
        self._maxEvents = maxEvents
        self._brancheNames = brancheNames

    def build(self, component):
        inputPath = os.path.join(getattr(component, self._analyzerName).path, self._fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self._treeName)
        if self._brancheNames is not None: self._disableAllUnnecessaryBranches(tree)
        return Events(tree, self._maxEvents)

    def _disableAllUnnecessaryBranches(self, tree):
        tree.SetBranchStatus('*', 0)
        for b in self._brancheNames:
            tree.SetBranchStatus(b, 1)

##____________________________________________________________________________||
