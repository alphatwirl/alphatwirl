# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
from ..Events import Events

##__________________________________________________________________||
class EventBuilder(object):
    def __init__(self, chunk):
        self.chunk = chunk

    def __call__(self):
        file = ROOT.TFile.Open(self.chunk.inputPath)
        tree = file.Get(self.chunk.treeName)
        events = Events(tree, self.chunk.maxEvents, self.chunk.start)
        events.chunk = self.chunk
        events.component = self.chunk.component
        return events

##__________________________________________________________________||
