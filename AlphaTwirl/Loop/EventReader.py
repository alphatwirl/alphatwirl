# Tai Sakuma <tai.sakuma@cern.ch>
from .EventLoop import EventLoop
from .Associator import Associator

##__________________________________________________________________||
class EventReader(object):
    """This class manages objects involved in reading data sets.

    On receiving a data set, this class calls the function
    split_into_build_events(), which splits the data set into chunks,
    creates the function build_events() for each chunk, and returns a
    list of the functions. Then, for each build_events(), This class
    creates a reader associated with the collector, creates an event
    loop, and send it to the event loop runner.

    """
    def __init__(self, eventLoopRunner, reader, collector,
                 split_into_build_events):

        self.eventLoopRunner = eventLoopRunner
        self.associator = Associator(reader, collector)
        self.reader = reader
        self.collector = collector
        self.split_into_build_events = split_into_build_events
        self.EventLoop = EventLoop

    def __repr__(self):
        return '{}(eventLoopRunner = {!r}, reader = {!r}, collector = {!r}, split_into_build_events = {!r})'.format(
            self.__class__.__name__,
            self.eventLoopRunner,
            self.reader,
            self.collector,
            self.split_into_build_events
        )

    def begin(self):
        self.eventLoopRunner.begin()

    def read(self, dataset):
        build_events_list = self.split_into_build_events(dataset)
        for build_events in build_events_list:
            reader = self.associator.make(dataset.name)
            eventLoop = self.EventLoop(build_events, reader)
            self.eventLoopRunner.run(eventLoop)

    def end(self):
        self.eventLoopRunner.end()
        return self.collector.collect()

##__________________________________________________________________||
