# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
from .DelphesEvents import DelphesEvents

##__________________________________________________________________||
class DelphesEventBuilder(object):
    def __init__(self, config):
        self.config = config

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self.config
        )

    def __call__(self):
        file = ROOT.TFile.Open(self.config.inputPath)
        tree = file.Get(self.config.treeName)
        events = DelphesEvents(tree, self.config.maxEvents, self.config.start)
        events.config = self.config
        return events

##__________________________________________________________________||
