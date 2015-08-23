from AlphaTwirl.EventReader import EventReader
import unittest

##__________________________________________________________________||
class MockEventBuilder(object):
    def build(self, dataset):
        return dataset._events

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, name = None):
        self.name = name
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self):
        self.collected = False

        self._datasetReaderPairs = [ ]

    def addReader(self, datasetName, reader):
        self._datasetReaderPairs.append((datasetName, reader))

    def collect(self):
        self.collected = True
        return 1234

##__________________________________________________________________||
class MockDataset(object):
    def __init__(self):
        self._events = None

##__________________________________________________________________||
class MockEventLoopRunner(object):
    def __init__(self):
        self.began = False
        self.ended = False
        self.eventLoop = None

    def begin(self):
        self.began = True

    def run(self, eventLoop):
        self.eventLoop = eventLoop

    def end(self):
        self.ended = True

##__________________________________________________________________||
class MockEventLoop(object):
    def __init__(self, eventBuilder, dataset, reader):
        self.eventBuilder = eventBuilder
        self.dataset = dataset
        self.reader = reader

##__________________________________________________________________||
class TestEventReader(unittest.TestCase):

    def test_eventBuilder_passed_to_EventLoop(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector()
        eventReader = EventReader(eventBuilder, eventLoopRunner, reader, collector)
        eventReader.EventLoop = MockEventLoop

        dataset1 = MockDataset()
        dataset1.name = "dataset1"
        eventReader.read(dataset1)
        self.assertIs(eventBuilder, eventLoopRunner.eventLoop.eventBuilder)

    def test_eventLoopRunner_called(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector()
        eventReader = EventReader(eventBuilder, eventLoopRunner, reader, collector)
        eventReader.EventLoop = MockEventLoop

        self.assertFalse(eventLoopRunner.began)
        eventReader.begin()
        self.assertTrue(eventLoopRunner.began)

        self.assertIsNone(eventLoopRunner.eventLoop)
        dataset1 = MockDataset()
        dataset1.name = "dataset1"
        eventReader.read(dataset1)
        self.assertIs(dataset1, eventLoopRunner.eventLoop.dataset)
        self.assertIsInstance(eventLoopRunner.eventLoop, MockEventLoop)

        self.assertFalse(eventLoopRunner.ended)
        eventReader.end()
        self.assertTrue(eventLoopRunner.ended)

    def test_packages_read_and_collected(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        reader = MockReader()
        collector = MockCollector()
        eventReader = EventReader(eventBuilder, eventLoopRunner, reader, collector)
        eventReader.EventLoop = MockEventLoop

        eventReader.begin()

        dataset1 = MockDataset()
        dataset1.name = "dataset1"
        eventReader.read(dataset1)
        self.assertIs("dataset1", eventLoopRunner.eventLoop.dataset.name)
        self.assertEqual(collector._datasetReaderPairs[0][1], eventLoopRunner.eventLoop.reader)

        dataset2 = MockDataset()
        dataset2.name = "dataset2"
        eventReader.read(dataset2)
        self.assertIs("dataset2", eventLoopRunner.eventLoop.dataset.name)
        self.assertEqual(collector._datasetReaderPairs[1][1], eventLoopRunner.eventLoop.reader)

        self.assertFalse(collector.collected)
        self.assertEqual(1234, eventReader.end())
        self.assertTrue(collector.collected)

##__________________________________________________________________||
