# Tai Sakuma <tai.sakuma@gmail.com>
import ROOT
from .DelphesEvents import DelphesEvents

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='alphatwirl.delphes has been moved to https://github.com/alphatwirl/atdelphes.')
class DelphesEventBuilder(object):
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
        events = DelphesEvents(chain, self.config.maxEvents, self.config.start)
        events.config = self.config
        return events

##__________________________________________________________________||
