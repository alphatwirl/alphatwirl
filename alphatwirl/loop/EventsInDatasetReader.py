# Tai Sakuma <tai.sakuma@cern.ch>
import copy

from .EventLoop import EventLoop

##__________________________________________________________________||
class EventsInDatasetReader(object):
    """This class manages objects involved in reading events in data sets.

    On receiving a data set, this class calls the function
    split_into_build_events(), which splits the data set into chunks,
    creates the function build_events() for each chunk, and returns a
    list of the functions. Then, for each build_events(), This class
    creates a copy of the reader, creates an event loop, and send it
    to the event loop runner.

    At the end, this class receives results from the event loop runner
    and have the collector collect them.

    """
    def __init__(self, eventLoopRunner, reader, collector,
                 split_into_build_events):

        self.eventLoopRunner = eventLoopRunner
        self.reader = reader
        self.collector = collector
        self.split_into_build_events = split_into_build_events

        self.EventLoop = EventLoop

        self.dataset_names = [ ]

    def __repr__(self):
        name_value_pairs = (
            ('eventLoopRunner',         self.eventLoopRunner),
            ('reader',                  self.reader),
            ('collector',               self.collector),
            ('split_into_build_events', self.split_into_build_events),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self):
        self.eventLoopRunner.begin()
        self.dataset_names = [ ]

    def read(self, dataset):
        build_events_list = self.split_into_build_events(dataset)
        for build_events in build_events_list:
            self.dataset_names.append(dataset.name)
            reader = copy.deepcopy(self.reader)
            eventLoop = self.EventLoop(build_events, reader)
            self.eventLoopRunner.run(eventLoop)

    def end(self):
        returned_readers = self.eventLoopRunner.end()

        if len(self.dataset_names) != len(returned_readers):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                'the same number of the readers were not returned: {} readers sent, {} readers returned. cannot collect results'.format(
                    len(self.dataset_names),
                    len(returned_readers)
                ))
            return None

        dataset_reader_pairs = zip(self.dataset_names, returned_readers)
        return self.collector.collect(dataset_reader_pairs)

##__________________________________________________________________||
