# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import itertools
from operator import itemgetter

from .EventLoop import EventLoop

##__________________________________________________________________||
class EventDatasetReader(object):
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

        self.dataset_nreaders = [ ]
        self.dataset_runids = [ ]

    def __repr__(self):
        name_value_pairs = (
            ('eventLoopRunner',         self.eventLoopRunner),
            ('reader',                  self.reader),
            ('collector',               self.collector),
            ('split_into_build_events', self.split_into_build_events),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self):
        self.eventLoopRunner.begin()
        self.dataset_nreaders = [ ]
        self.runids = [ ]

    def read(self, dataset):
        build_events_list = self.split_into_build_events(dataset)
        self.dataset_nreaders.append((dataset, len(build_events_list)))
        eventLoops = [ ]
        for build_events in build_events_list:
            reader = copy.deepcopy(self.reader)
            eventLoop = self.EventLoop(build_events, reader, dataset.name)
            eventLoops.append(eventLoop)
        runids = self.eventLoopRunner.run_multiple(eventLoops)
        self.dataset_runids.append((dataset, runids))

    def end(self):

        runids_towait = list(itertools.chain(*[ids for _, ids in self.dataset_runids]))
        returned = [ ]
        while runids_towait:
            r_ = self.eventLoopRunner.poll()
            ids_ = [i for i, _ in r_]
            runids_towait = [i for i in runids_towait if i not in ids_]
            returned.extend(r_)
        returned = sorted(returned, key=itemgetter(0))
        returned_readers = [r for _, r in returned]

        nreaders_total = sum((n for _, n in self.dataset_nreaders))

        if nreaders_total != len(returned_readers):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                'the same number of the readers were not returned: {} readers sent, {} readers returned. cannot collect results'.format(
                    nreaders_total,
                    len(returned_readers)
                ))
            return None

        dataset_readers_list = [ ]
        i = 0
        for dataset, nreaders in self.dataset_nreaders:
            dataset_readers_list.append((dataset.name, tuple(returned_readers[i:(i + nreaders)])))
            i += nreaders

        dataset_merged_readers_list = [ ]
        for dataset, readers in dataset_readers_list:
            reader = copy.deepcopy(self.reader)
            dataset_merged_readers_list.append((dataset, [reader]))
            if not hasattr(reader, 'merge'):
                continue
            for r in readers:
                reader.merge(r)

        return self.collector.collect(dataset_merged_readers_list)

##__________________________________________________________________||
