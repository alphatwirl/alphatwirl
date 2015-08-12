# Tai Sakuma <tai.sakuma@cern.ch>
from .EventLoop import EventLoop
from .Associator import Associator

##__________________________________________________________________||
class AllEvents(object):
    def __call__(self, event): return True

##__________________________________________________________________||
class EventReader(object):
    def __init__(self, eventBuilder, eventLoopRunner, reader, collector, eventSelection = None):
        self.eventBuilder = eventBuilder
        self.eventLoopRunner = eventLoopRunner
        self.associator = Associator(reader, collector)
        self.collector = collector

        self.eventSelection = eventSelection if eventSelection is not None else AllEvents()

        self.EventLoop = EventLoop

    def begin(self):
        self.eventLoopRunner.begin()

    def read(self, dataset):
        reader = self.associator.make(dataset.name)
        eventLoop = self.EventLoop(self.eventBuilder, self.eventSelection, dataset, reader)
        self.eventLoopRunner.run(eventLoop)

    def end(self):
        self.eventLoopRunner.end()
        return self.collector.collect()

##__________________________________________________________________||
