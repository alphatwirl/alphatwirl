from AlphaTwirl.EventReader import EventReaderBundle
import unittest

##____________________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

##____________________________________________________________________________||
class MockEventSelection(object): pass

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##____________________________________________________________________________||
class MockReaderPackage(object):
    def __init__(self):
        self.reader = None
        self.collected = False

    def make(self, name):
        self.reader = MockReader(name)
        return self.reader

    def collect(self):
        self.collected = True

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self):
        self._events = None

##____________________________________________________________________________||
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

##____________________________________________________________________________||
class MockEventLoop(object):
    def __init__(self, eventBuilder, eventSelection, component, readers):
        self.eventBuilder = eventBuilder
        self.component = component
        self.readers = readers
        self.eventSelection = eventSelection

##____________________________________________________________________________||
class TestEventReaderEventReaderBundle(unittest.TestCase):

    def test_eventBuilder_passed_to_EventLoop(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner)
        bundle.EventLoop = MockEventLoop

        component1 = MockComponent()
        bundle.read(component1)
        self.assertIs(eventBuilder, eventLoopRunner.eventLoop.eventBuilder)

    def test_eventSelection_passed_to_EventLoop(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        eventSelection = MockEventSelection()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner, eventSelection)
        bundle.EventLoop = MockEventLoop

        component1 = MockComponent()
        bundle.read(component1)
        self.assertIs(eventSelection, eventLoopRunner.eventLoop.eventSelection)

    def test_eventLoopRunner_called(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner)
        bundle.EventLoop = MockEventLoop

        self.assertFalse(eventLoopRunner.began)
        bundle.begin()
        self.assertTrue(eventLoopRunner.began)

        self.assertIsNone(eventLoopRunner.eventLoop)
        component1 = MockComponent()
        bundle.read(component1)
        self.assertIs(component1, eventLoopRunner.eventLoop.component)
        self.assertIsInstance(eventLoopRunner.eventLoop, MockEventLoop)

        self.assertFalse(eventLoopRunner.ended)
        bundle.end()
        self.assertTrue(eventLoopRunner.ended)


    def test_packages_read_and_collected(self):
        eventBuilder = MockEventBuilder()
        eventLoopRunner = MockEventLoopRunner()
        bundle = EventReaderBundle(eventBuilder, eventLoopRunner)
        bundle.EventLoop = MockEventLoop

        package1 = MockReaderPackage()
        bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        bundle.addReaderPackage(package2)

        bundle.begin()

        component1 = MockComponent()
        component1.name = "compName1"
        bundle.read(component1)
        self.assertIs("compName1", eventLoopRunner.eventLoop.component.name)
        self.assertEqual([package1.reader, package2.reader],eventLoopRunner.eventLoop.readers)

        component2 = MockComponent()
        component2.name = "compName2"
        bundle.read(component2)
        self.assertIs("compName2", eventLoopRunner.eventLoop.component.name)
        self.assertEqual([package1.reader, package2.reader],eventLoopRunner.eventLoop.readers)

        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        bundle.end()
        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)


##____________________________________________________________________________||
