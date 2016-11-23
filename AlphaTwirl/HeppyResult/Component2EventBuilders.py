# Tai Sakuma <tai.sakuma@cern.ch>
from .ComponentSplitter import ComponentSplitter

##__________________________________________________________________||
class Component2EventBuilders(object):
    """Split a component into instances of EventBuilder
    """
    def __init__(self, componentSplitter, EventBuilder):
        self.splitter = componentSplitter
        self.EventBuilder = EventBuilder

    def __call__(self, component):
        chunks = self.splitter.split(component)
        eventBuilders = [self.EventBuilder(c) for c in chunks]
        return eventBuilders

##__________________________________________________________________||
