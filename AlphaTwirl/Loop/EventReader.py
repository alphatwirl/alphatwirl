# Tai Sakuma <tai.sakuma@cern.ch>
from .EventLoop import EventLoop
from .Associator import Associator

##__________________________________________________________________||
class EventReader(object):
    """This class manages objects involved in reading data sets.

    On receiving a data set, this class splits it into chunks. Then,
    for each chunk, it creates a reader associated with the collector,
    creates an event loop, and send it to the event loop runner.

    """
    def __init__(self, eventBuilder, eventLoopRunner, reader, collector, datasetSplitter):

        self.eventBuilder = eventBuilder
        self.eventLoopRunner = eventLoopRunner
        self.associator = Associator(reader, collector)
        self.collector = collector
        self.splitter = datasetSplitter
        self.EventLoop = EventLoop

    def begin(self):
        self.eventLoopRunner.begin()

    def read(self, dataset):
        chunks = self.splitter.split(dataset)
        for chunk in chunks:
            reader = self.associator.make(dataset.name)
            eventLoop = self.EventLoop(self.eventBuilder, chunk, reader)
            self.eventLoopRunner.run(eventLoop)

    def end(self):
        self.eventLoopRunner.end()
        return self.collector.collect()

##__________________________________________________________________||
