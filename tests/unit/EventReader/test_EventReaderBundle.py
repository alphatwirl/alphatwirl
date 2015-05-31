from AlphaTwirl.EventReader import EventReaderBundle
import unittest

##__________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

##__________________________________________________________________||
class MockEventSelection(object): pass

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self):
        self.collected = False

    def collect(self):
        self.collected = True
        return 1234

##__________________________________________________________________||
class MockEventReaderCollectorAssociator(object):
    def __init__(self):
        self.reader = None
        self.collector = MockCollector()

    def make(self, name):
        self.reader = MockReader(name)
        return self.reader

##__________________________________________________________________||
class MockComponent(object):
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
    def __init__(self, eventBuilder, eventSelection, component, reader):
        self.eventBuilder = eventBuilder
        self.component = component
        self.reader = reader
        self.eventSelection = eventSelection

##__________________________________________________________________||
class TestEventReaderBundle(unittest.TestCase):

    def test_eventBuilder_passed_to_EventLoop(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        readerCollectorAssociator = MockEventReaderCollectorAssociator()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner, readerCollectorAssociator)
        bundle.EventLoop = MockEventLoop

        component1 = MockComponent()
        component1.name = "compName1"
        bundle.read(component1)
        self.assertIs(eventBuilder, eventLoopRunner.eventLoop.eventBuilder)

    def test_eventSelection_passed_to_EventLoop(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        readerCollectorAssociator = MockEventReaderCollectorAssociator()
        eventSelection = MockEventSelection()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner, readerCollectorAssociator, eventSelection)
        bundle.EventLoop = MockEventLoop

        component1 = MockComponent()
        component1.name = "compName1"
        bundle.read(component1)
        self.assertIs(eventSelection, eventLoopRunner.eventLoop.eventSelection)

    def test_eventLoopRunner_called(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        readerCollectorAssociator = MockEventReaderCollectorAssociator()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner, readerCollectorAssociator)
        bundle.EventLoop = MockEventLoop

        self.assertFalse(eventLoopRunner.began)
        bundle.begin()
        self.assertTrue(eventLoopRunner.began)

        self.assertIsNone(eventLoopRunner.eventLoop)
        component1 = MockComponent()
        component1.name = "compName1"
        bundle.read(component1)
        self.assertIs(component1, eventLoopRunner.eventLoop.component)
        self.assertIsInstance(eventLoopRunner.eventLoop, MockEventLoop)

        self.assertFalse(eventLoopRunner.ended)
        bundle.end()
        self.assertTrue(eventLoopRunner.ended)

    def test_packages_read_and_collected(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        readerCollectorAssociator = MockEventReaderCollectorAssociator()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner, readerCollectorAssociator)
        bundle.EventLoop = MockEventLoop

        bundle.begin()

        component1 = MockComponent()
        component1.name = "compName1"
        bundle.read(component1)
        self.assertIs("compName1", eventLoopRunner.eventLoop.component.name)
        self.assertEqual(readerCollectorAssociator.reader, eventLoopRunner.eventLoop.reader)

        component2 = MockComponent()
        component2.name = "compName2"
        bundle.read(component2)
        self.assertIs("compName2", eventLoopRunner.eventLoop.component.name)
        self.assertEqual(readerCollectorAssociator.reader,eventLoopRunner.eventLoop.reader)

        self.assertFalse(readerCollectorAssociator.collector.collected)
        self.assertEqual(1234, bundle.end())
        self.assertTrue(readerCollectorAssociator.collector.collected)

##__________________________________________________________________||
