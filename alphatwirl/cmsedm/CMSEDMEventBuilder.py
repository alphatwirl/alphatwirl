# Tai Sakuma <tai.sakuma@cern.ch>
from .CMSEDMEvents import CMSEDMEvents

##__________________________________________________________________||
class CMSEDMEventBuilder(object):
    def __init__(self, config):
        self.config = config

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self.config
        )

    def __call__(self):
        events = CMSEDMEvents(
            paths = self.config.inputPaths,
            maxEvents = self.config.maxEvents,
            start = self.config.start
        )
        events.config = self.config
        events.dataset = self.config.dataset.name
        return events

##__________________________________________________________________||
