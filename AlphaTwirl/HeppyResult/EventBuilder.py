# Tai Sakuma <tai.sakuma@cern.ch>
import os
import ROOT
from ..Events import Events

##__________________________________________________________________||
class EventBuilder(object):
    def __init__(self, analyzerName, fileName, treeName, maxEvents = -1, brancheNames = None):
        self._analyzerName = analyzerName
        self._fileName = fileName
        self._treeName = treeName
        self._maxEvents = maxEvents
        self._brancheNames = brancheNames

    def getNumberOfEventsInDataset(self, component):
        inputPath = os.path.join(getattr(component, self._analyzerName).path, self._fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self._treeName)
        return self._minimumPositiveValue([self._maxEvents, tree.GetEntries()])

    def build(self, component, start = 0, nEvents = -1):
        inputPath = os.path.join(getattr(component, self._analyzerName).path, self._fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self._treeName)
        if self._brancheNames is not None: self._disableAllUnnecessaryBranches(tree)
        maxEvents = self._minimumPositiveValue([self._maxEvents, nEvents])
        ret = Events(tree, maxEvents, start)
        ret.component = component
        return ret

    def _minimumPositiveValue(self, vals):
        vals = [v for v in vals if v >= 0]
        if not vals: return -1
        return min(vals)

    def _disableAllUnnecessaryBranches(self, tree):
        tree.SetBranchStatus('*', 0)
        for b in self._brancheNames:
            tree.SetBranchStatus(b, 1)

##__________________________________________________________________||
