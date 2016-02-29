# Tai Sakuma <tai.sakuma@cern.ch>
import os
import ROOT
from ..Events import BEvents

##__________________________________________________________________||
class BEventBuilder(object):
    def __init__(self, analyzerName, fileName, treeName, maxEvents = -1):
        self._analyzerName = analyzerName
        self._fileName = fileName
        self._treeName = treeName
        self._maxEvents = maxEvents

    def getNumberOfEventsInDataset(self, component):
        inputPath = os.path.join(getattr(component, self._analyzerName).path, self._fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self._treeName)
        return self._minimumPositiveValue([self._maxEvents, tree.GetEntries()])

    def build(self, component, start = 0, nEvents = -1):
        inputPath = os.path.join(getattr(component, self._analyzerName).path, self._fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self._treeName)
        maxEvents = self._minimumPositiveValue([self._maxEvents, nEvents])
        ret = BEvents(tree, maxEvents, start)
        ret.component = component
        return ret

    def _minimumPositiveValue(self, vals):
        vals = [v for v in vals if v >= 0]
        if not vals: return -1
        return min(vals)

##__________________________________________________________________||
