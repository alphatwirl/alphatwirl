import unittest
import collections

from alphatwirl.loop import EventsInDatasetReader

##__________________________________________________________________||
MockEventBuilder = collections.namedtuple('MockEventBuilder', 'events')

##__________________________________________________________________||
class MockReader(object): pass

##__________________________________________________________________||
class MockCollectorReturn(object): pass

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self, ret = None):
        self.collected = None
        self.ret = ret

    def collect(self, dataset_readers_list):
        self.collected = dataset_readers_list
        return self.ret

##__________________________________________________________________||
MockDataset = collections.namedtuple('MockDataset', 'name build_events')

##__________________________________________________________________||
MockEventLoop = collections.namedtuple('MockEventLoop', 'build_events reader')

##__________________________________________________________________||
def mock_split_into_build_events(dataset):
    return dataset.build_events

##__________________________________________________________________||
class MockEventLoopRunner(object):
    def __init__(self):
        self.began = False
        self.ended = False
        self.eventLoops = [ ]

    def begin(self):
        self.began = True

    def run(self, eventLoop):
        self.eventLoops.append(eventLoop)

    def end(self):
        self.ended = True
        return [l.reader for l in self.eventLoops]

##__________________________________________________________________||
class TestEventsInDatasetReader(unittest.TestCase):

    def setUp(self):
        self.eventLoopRunner = MockEventLoopRunner()
        self.reader = MockReader()
        self.collector = MockCollector(MockCollectorReturn())
        self.obj = EventsInDatasetReader(self.eventLoopRunner, self.reader, self.collector, mock_split_into_build_events)
        self.obj.EventLoop = MockEventLoop

    def test_repr(self):
        repr(self.obj)

    def test_begin(self):
        self.assertFalse(self.eventLoopRunner.began)
        self.obj.begin()
        self.assertTrue(self.eventLoopRunner.began)

    def test_end(self):
        self.obj.begin()
        self.obj.end()

    def test_end_without_begin(self):
        self.obj.end()

    def test_wrong_number_of_results(self):

        build_events1 = MockEventBuilder('events1')
        eventLoop1 = MockEventLoop(build_events1, MockReader())
        build_events2 = MockEventBuilder('events2')
        eventLoop2 = MockEventLoop(build_events2, MockReader())
        self.eventLoopRunner.run(eventLoop1)
        self.eventLoopRunner.run(eventLoop2)

        dataset1 = MockDataset('dataset1', (build_events1, build_events2))

        self.obj.dataset_nreaders[:] = [(dataset1, 1)]
        self.assertIsNone(self.obj.end())

    def test_standard(self):

        ## begin
        self.obj.begin()

        ## create data sets
        # dataset1 - 3 event builders
        build_events1 = MockEventBuilder('events1')
        build_events2 = MockEventBuilder('events2')
        build_events3 = MockEventBuilder('events3')
        dataset1 = MockDataset('dataset1', (build_events1, build_events2, build_events3))

        # dataset2 - no event builder
        dataset2 = MockDataset('dataset2', ( ))

        # dataset3 - 1 event builder
        build_events4 = MockEventBuilder('events4')
        dataset3 = MockDataset('dataset3', (build_events4, ))

        ## read
        self.obj.read(dataset1)
        self.obj.read(dataset2)
        self.obj.read(dataset3)

        # assert eventLoopRunner has received eventLoops with correct
        # event builders and readers
        self.assertEqual(4, len(self.eventLoopRunner.eventLoops))

        eventLoop1 = self.eventLoopRunner.eventLoops[0]
        self.assertIsInstance(eventLoop1, MockEventLoop)
        self.assertIs(build_events1, eventLoop1.build_events)
        self.assertIsInstance(eventLoop1.reader, MockReader)

        eventLoop2 = self.eventLoopRunner.eventLoops[1]
        self.assertIsInstance(eventLoop2, MockEventLoop)
        self.assertIs(build_events2, eventLoop2.build_events)
        self.assertIsInstance(eventLoop2.reader, MockReader)

        eventLoop3 = self.eventLoopRunner.eventLoops[2]
        self.assertIsInstance(eventLoop3, MockEventLoop)
        self.assertIs(build_events3, eventLoop3.build_events)
        self.assertIsInstance(eventLoop3.reader, MockReader)

        eventLoop4 = self.eventLoopRunner.eventLoops[3]
        self.assertIsInstance(eventLoop4, MockEventLoop)
        self.assertIs(build_events4, eventLoop4.build_events)
        self.assertIsInstance(eventLoop4.reader, MockReader)

        ## end
        self.assertFalse(self.eventLoopRunner.ended)
        self.assertIsNone(self.collector.collected)
        self.assertIs(self.collector.ret, self.obj.end())
        self.assertTrue(self.eventLoopRunner.ended)

        expected = [
            ('dataset1', (eventLoop1.reader, eventLoop2.reader, eventLoop3.reader), ),
            ('dataset2', ( )),
            ('dataset3', (eventLoop4.reader, )),
            ]

        # this asserts the readers are the same python objects
        self.assertEqual(expected, self.collector.collected)
##__________________________________________________________________||
