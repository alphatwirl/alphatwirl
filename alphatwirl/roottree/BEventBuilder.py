# Tai Sakuma <tai.sakuma@gmail.com>
from .BEvents import BEvents
from .EventBuilder import EventBuilder

##__________________________________________________________________||
class BEventBuilder(EventBuilder):
    def __init__(self, config):
        super(BEventBuilder, self).__init__(config, EventsClass=BEvents)

##__________________________________________________________________||
