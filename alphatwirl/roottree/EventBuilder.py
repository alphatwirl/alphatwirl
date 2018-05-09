# Tai Sakuma <tai.sakuma@gmail.com>
import logging

import ROOT

from .Events import Events
from .inspect import is_ROOT_null_pointer

##__________________________________________________________________||
class EventBuilder(object):
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
            file_ = ROOT.TFile.Open(path)
            if is_ROOT_null_pointer(file_) or file_.IsZombie():
                logger = logging.getLogger(__name__)
                logger.error('cannot open {}'.format(path))
                raise OSError('cannot open {}'.format(path))
            chain.Add(path)
        events = Events(chain, self.config.maxEvents, self.config.start)
        events.config = self.config
        return events

##__________________________________________________________________||
