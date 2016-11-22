# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
from ..Events import Events

##__________________________________________________________________||
class EventBuilder(object):

    def build(self, chunk):
        file = ROOT.TFile.Open(chunk.inputPath)
        tree = file.Get(chunk.treeName)
        ret = Events(tree, chunk.maxEvents, chunk.start)
        ret.chunk = chunk
        ret.component = chunk.component
        return ret

##__________________________________________________________________||
