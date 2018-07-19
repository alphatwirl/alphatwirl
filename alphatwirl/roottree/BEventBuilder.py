# Tai Sakuma <tai.sakuma@gmail.com>
from .BEvents import BEvents
from .EventBuilder import EventBuilder

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='use BuildEvents instead')
class BEventBuilder(EventBuilder):
    def __init__(self, config):
        super(BEventBuilder, self).__init__(config, EventsClass=BEvents)

##__________________________________________________________________||
