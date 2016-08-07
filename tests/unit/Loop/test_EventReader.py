from AlphaTwirl.Loop import EventReader
import unittest

##__________________________________________________________________||
class MockEventBuilder(object):
    def __init__(self, nEntries = None):
        self.nEntries = nEntries

    def getNumberOfEventsInDataset(self, dataset):
        return self.nEntries

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
        self.datasetName = datasetName
        self.reader = reader

    def collect(self):
        self.collected = True
        return self.ret

##__________________________________________________________________||
class MockDataset(object): pass

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
    def __init__(self, eventBuilder, dataset, reader, start = None, nEvents = None):
        self.eventBuilder = eventBuilder
        self.dataset = dataset
        self.reader = reader
        self.start = start
        self.nEvents = nEvents

##__________________________________________________________________||
class TestEventReader(unittest.TestCase):

    def test_standard(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector(MockCollectorReturn())
        obj = EventReader(eventBuilder, eventLoopRunner, reader, collector)
        obj.EventLoop = MockEventLoop

        # begin
        self.assertFalse(eventLoopRunner.began)
        obj.begin()
        self.assertTrue(eventLoopRunner.began)

        # read
        dataset1 = MockDataset()
        dataset1.name = "dataset1"
        obj.read(dataset1)
        self.assertEqual(1, len(eventLoopRunner.eventLoops))
        eventLoop1 =  eventLoopRunner.eventLoops[0]
        self.assertIsInstance(eventLoop1, MockEventLoop)
        self.assertIs(eventBuilder, eventLoop1.eventBuilder)
        self.assertIs(dataset1, eventLoop1.dataset)
        self.assertIsInstance(eventLoop1.reader, MockReader)
        self.assertIsNone(eventLoop1.start)
        self.assertIsNone(eventLoop1.nEvents)

        self.assertEqual("dataset1", collector.datasetName)
        self.assertIs(eventLoop1.reader, collector.reader)

        # end
        self.assertFalse(eventLoopRunner.ended)
        self.assertFalse(collector.collected)
        self.assertIs(collector.ret, obj.end())
        self.assertTrue(eventLoopRunner.ended)
        self.assertTrue(collector.collected)

    def test_init_raise(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector(MockCollectorReturn())
        self.assertRaises(ValueError, EventReader, eventBuilder, eventLoopRunner, reader, collector, maxEventsPerRun = 0)

    def test_split_dataset(self):
        eventBuilder = MockEventBuilder(nEntries = 25)
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector(MockCollectorReturn())
        obj = EventReader(eventBuilder, eventLoopRunner, reader, collector, maxEventsPerRun = 10)
        obj.EventLoop = MockEventLoop

        # begin
        self.assertFalse(eventLoopRunner.began)
        obj.begin()
        self.assertTrue(eventLoopRunner.began)

        # read
        dataset1 = MockDataset()
        dataset1.name = "dataset1"
        obj.read(dataset1)

        self.assertEqual(3, len(eventLoopRunner.eventLoops))
        self.assertEqual(3, len(collector.pairs))

        eventLoop =  eventLoopRunner.eventLoops[0]
        self.assertIsInstance(eventLoop, MockEventLoop)
        self.assertIs(eventBuilder, eventLoop.eventBuilder)
        self.assertIs(dataset1, eventLoop.dataset)
        self.assertIsInstance(eventLoop.reader, MockReader)
        self.assertEqual(0, eventLoop.start)
        self.assertEqual(10, eventLoop.nEvents)

        self.assertEqual(("dataset1", eventLoop.reader), collector.pairs[0])

        eventLoop =  eventLoopRunner.eventLoops[1]
        self.assertIsInstance(eventLoop, MockEventLoop)
        self.assertIs(eventBuilder, eventLoop.eventBuilder)
        self.assertIs(dataset1, eventLoop.dataset)
        self.assertIsInstance(eventLoop.reader, MockReader)
        self.assertEqual(10, eventLoop.start)
        self.assertEqual(10, eventLoop.nEvents)

        self.assertEqual(("dataset1", eventLoop.reader), collector.pairs[1])

        eventLoop =  eventLoopRunner.eventLoops[2]
        self.assertIsInstance(eventLoop, MockEventLoop)
        self.assertIs(eventBuilder, eventLoop.eventBuilder)
        self.assertIs(dataset1, eventLoop.dataset)
        self.assertIsInstance(eventLoop.reader, MockReader)
        self.assertEqual(20, eventLoop.start)
        self.assertEqual(5, eventLoop.nEvents)

        self.assertEqual(("dataset1", eventLoop.reader), collector.pairs[2])

        # end
        self.assertFalse(eventLoopRunner.ended)
        self.assertFalse(collector.collected)
        self.assertIs(collector.ret, obj.end())
        self.assertTrue(eventLoopRunner.ended)
        self.assertTrue(collector.collected)

    def test_create_start_nEvents_list(self):
        obj = EventReader(MockEventBuilder(), MockEventLoopRunner(), MockReader(), MockCollector())
        self.assertEqual([(0, 10), (10, 10), (20, 10), (30, 10)], obj._create_start_nEvents_list(40, 10))
        self.assertEqual([(0, 10), (10, 10), (20, 10), (30, 10), (40, 1)], obj._create_start_nEvents_list(41, 10))
        self.assertEqual([(0, 40)], obj._create_start_nEvents_list(40, 40))
        self.assertEqual([(0, 40)], obj._create_start_nEvents_list(40, 50))

##__________________________________________________________________||
