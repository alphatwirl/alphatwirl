import unittest

from AlphaTwirl.Loop import EventReader

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

##__________________________________________________________________||
class MockEventLoop(object):
    def __init__(self, build_events, reader):
        self.build_events = build_events
        self.reader = reader

##__________________________________________________________________||
class TestEventReader(unittest.TestCase):

    def test_repr(self):
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector(MockCollectorReturn())
        obj = EventReader(eventLoopRunner, reader, collector, mock_split_into_build_events)
        repr(obj)

    def test_standard(self):
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector(MockCollectorReturn())
        obj = EventReader(eventLoopRunner, reader, collector, mock_split_into_build_events)
        obj.EventLoop = MockEventLoop

        # begin
        self.assertFalse(eventLoopRunner.began)
        obj.begin()
        self.assertTrue(eventLoopRunner.began)

        # read
        dataset1 = MockDataset()
        dataset1.name = "dataset1"
        build_events1 = MockEventBuilder()
        build_events2 = MockEventBuilder()
        build_events3 = MockEventBuilder()
        dataset1.build_events = [build_events1, build_events2, build_events3]
        obj.read(dataset1)

        self.assertEqual(3, len(eventLoopRunner.eventLoops))

        eventLoop1 =  eventLoopRunner.eventLoops[0]
        self.assertIsInstance(eventLoop1, MockEventLoop)
        self.assertIs(build_events1, eventLoop1.build_events)
        self.assertIsInstance(eventLoop1.reader, MockReader)

        self.assertEqual("dataset1", collector.pairs[0][0])
        self.assertIs(eventLoop1.reader, collector.pairs[0][1])

        eventLoop2 =  eventLoopRunner.eventLoops[1]
        self.assertIsInstance(eventLoop2, MockEventLoop)
        self.assertIs(build_events2, eventLoop2.build_events)
        self.assertIsInstance(eventLoop2.reader, MockReader)

        self.assertEqual("dataset1", collector.pairs[1][0])
        self.assertIs(eventLoop2.reader, collector.pairs[1][1])

        eventLoop3 =  eventLoopRunner.eventLoops[2]
        self.assertIsInstance(eventLoop3, MockEventLoop)
        self.assertIs(build_events3, eventLoop3.build_events)
        self.assertIsInstance(eventLoop3.reader, MockReader)

        self.assertEqual("dataset1", collector.pairs[2][0])
        self.assertIs(eventLoop3.reader, collector.pairs[2][1])

        # end
        self.assertFalse(eventLoopRunner.ended)
        self.assertFalse(collector.collected)
        self.assertIs(collector.ret, obj.end())
        self.assertTrue(eventLoopRunner.ended)
        self.assertTrue(collector.collected)

##__________________________________________________________________||
