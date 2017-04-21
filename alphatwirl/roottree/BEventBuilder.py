# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
from .BEvents import BEvents

##__________________________________________________________________||
class BEventBuilder(object):
    def __init__(self, config):
        self.config = config

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self.config
        )

    def __call__(self):
        chain = ROOT.TChain(self.config.treeName)
        for path in self.config.inputPaths:
            chain.Add(path)
        events = BEvents(chain, self.config.maxEvents, self.config.start)
        events.config = self.config
        return events

##__________________________________________________________________||
