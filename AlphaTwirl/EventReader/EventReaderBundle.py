# Tai Sakuma <tai.sakuma@cern.ch>
from EventLoop import EventLoop

##__________________________________________________________________||
class AllEvents(object):
    def __call__(self, event): return True

##__________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder, eventLoopRunner, readerPackage, eventSelection = None):
        self.eventBuilder = eventBuilder
        self.eventLoopRunner = eventLoopRunner
        self.readerPackage = readerPackage
        self.eventSelection = eventSelection if eventSelection is not None else AllEvents()

        self.EventLoop = EventLoop

    def begin(self):
        self.eventLoopRunner.begin()

    def read(self, component):
        readers = self.readerPackage.make(component.name)
        eventLoop = self.EventLoop(self.eventBuilder, self.eventSelection, component, readers)
        self.eventLoopRunner.run(eventLoop)

    def end(self):
        self.eventLoopRunner.end()
        self.readerPackage.collect()

##__________________________________________________________________||
