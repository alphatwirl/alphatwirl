import unittest

from alphatwirl.loop import EventReader

##__________________________________________________________________||
class MockEventBuilder(object): pass

##__________________________________________________________________||
class MockReader(object): pass

##__________________________________________________________________||
class MockCollectorReturn(object): pass

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self, ret = None):
        self.collected = False
        self.ret = ret

        self.pairs = [ ]

    def addReader(self, datasetName, reader):
        self.pairs.append((datasetName, reader))

    def collect(self):
        self.collected = True
        return self.ret

##__________________________________________________________________||
class MockDataset(object): pass

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
class MockEventLoop(object):
    def __init__(self, build_events, reader):
        self.build_events = build_events
        self.reader = reader

##__________________________________________________________________||
class TestEventReader(unittest.TestCase):

    def setUp(self):
        self.eventLoopRunner = MockEventLoopRunner()
        self.reader = MockReader()
        self.collector = MockCollector(MockCollectorReturn())
        self.obj = EventReader(self.eventLoopRunner, self.reader, self.collector, mock_split_into_build_events)

    def test_repr(self):
        repr(self.obj)

    def test_begin(self):
        self.obj.begin()

    def test_end(self):
        self.obj.begin()
        self.obj.end()

    def test_end_without_begin(self):
        self.obj.end()

    def test_wrong_number_of_results(self):
        self.obj.EventLoop = MockEventLoop

        build_events1 = MockEventBuilder()
        eventLoop1 = MockEventLoop(build_events1, MockReader())
        build_events2 = MockEventBuilder()
        eventLoop2 = MockEventLoop(build_events2, MockReader())
        self.eventLoopRunner.run(eventLoop1)
        self.eventLoopRunner.run(eventLoop2)

        self.obj.dataset_names[:] = ['dataset1']
        self.assertIsNone(self.obj.end())

    def test_standard(self):
        self.obj.EventLoop = MockEventLoop

        # begin
        self.assertFalse(self.eventLoopRunner.began)
        self.obj.begin()
        self.assertTrue(self.eventLoopRunner.began)

        # read
        dataset1 = MockDataset()
        dataset1.name = "dataset1"
        build_events1 = MockEventBuilder()
        build_events2 = MockEventBuilder()
        build_events3 = MockEventBuilder()
        dataset1.build_events = [build_events1, build_events2, build_events3]
        self.obj.read(dataset1)

        self.assertEqual(3, len(self.eventLoopRunner.eventLoops))

        eventLoop1 =  self.eventLoopRunner.eventLoops[0]
        self.assertIsInstance(eventLoop1, MockEventLoop)
        self.assertIs(build_events1, eventLoop1.build_events)
        self.assertIsInstance(eventLoop1.reader, MockReader)

        eventLoop2 =  self.eventLoopRunner.eventLoops[1]
        self.assertIsInstance(eventLoop2, MockEventLoop)
        self.assertIs(build_events2, eventLoop2.build_events)
        self.assertIsInstance(eventLoop2.reader, MockReader)

        eventLoop3 =  self.eventLoopRunner.eventLoops[2]
        self.assertIsInstance(eventLoop3, MockEventLoop)
        self.assertIs(build_events3, eventLoop3.build_events)
        self.assertIsInstance(eventLoop3.reader, MockReader)

        # end
        self.assertFalse(self.eventLoopRunner.ended)
        self.assertFalse(self.collector.collected)
        self.assertIs(self.collector.ret, self.obj.end())
        self.assertTrue(self.eventLoopRunner.ended)
        self.assertTrue(self.collector.collected)

        self.assertEqual("dataset1", self.collector.pairs[0][0])
        self.assertIs(eventLoop1.reader, self.collector.pairs[0][1])

        self.assertEqual("dataset1", self.collector.pairs[1][0])
        self.assertIs(eventLoop2.reader, self.collector.pairs[1][1])

        self.assertEqual("dataset1", self.collector.pairs[2][0])
        self.assertIs(eventLoop3.reader, self.collector.pairs[2][1])

##__________________________________________________________________||
