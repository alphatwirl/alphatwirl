# Tai Sakuma <tai.sakuma@gmail.com>
from .CMSEDMEvents import CMSEDMEvents

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='alphatwirl.cmsedm has been moved to https://github.com/alphatwirl/atcmsedm.')
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
