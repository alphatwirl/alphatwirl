from AlphaTwirl.EventReader import EventReader
import unittest

##__________________________________________________________________||
class MockEventBuilder(object): pass

##__________________________________________________________________||
class MockReader(object): pass

##__________________________________________________________________||
class MockCollectorReturn(object): pass

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self, ret):
        self.collected = False
        self.ret = ret

    def addReader(self, datasetName, reader):
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
        eventLoop1 =  eventLoopRunner.eventLoop
        self.assertIsInstance(eventLoop1, MockEventLoop)
        self.assertIs(eventBuilder, eventLoop1.eventBuilder)
        self.assertIs(dataset1, eventLoop1.dataset)
        self.assertIsInstance(eventLoop1.reader, MockReader)

        self.assertEqual("dataset1", collector.datasetName)
        self.assertIs(eventLoop1.reader, collector.reader)

        # end
        self.assertFalse(eventLoopRunner.ended)
        self.assertFalse(collector.collected)
        self.assertIs(collector.ret, obj.end())
        self.assertTrue(eventLoopRunner.ended)
        self.assertTrue(collector.collected)

##__________________________________________________________________||
