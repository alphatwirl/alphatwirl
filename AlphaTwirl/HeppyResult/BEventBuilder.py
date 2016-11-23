# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
from ..Events import BEvents

##__________________________________________________________________||
class BEventBuilder(object):
    def __init__(self, chunk):
        self.chunk = chunk

    def __call__(self):
        file = ROOT.TFile.Open(self.chunk.inputPath)
        tree = file.Get(self.chunk.treeName)
        events = BEvents(tree, self.chunk.maxEvents, self.chunk.start)
        events.chunk = self.chunk
        events.component = self.chunk.component
        return events

##__________________________________________________________________||
