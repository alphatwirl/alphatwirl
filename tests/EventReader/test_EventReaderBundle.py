from AlphaTwirl.EventReader import EventReaderBundle, EventLoop
import unittest

##____________________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

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
class TestEventReaderEventReaderBundle(unittest.TestCase):

    def setUp(self):
        self.eventBuilder = MockEventBuilder()
        self.eventLoopRunner = MockEventLoopRunner()
        self.bundle = EventReaderBundle(self.eventBuilder, self.eventLoopRunner)

    def test_begin_read_end(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

        self.assertFalse(self.eventLoopRunner.began)
        self.bundle.begin()
        self.assertTrue(self.eventLoopRunner.began)

        component1 = MockComponent()
        component1.name = "compName1"

        self.assertIsNone(self.eventLoopRunner.eventLoop)
        self.bundle.read(component1)

        self.assertIsInstance(self.eventLoopRunner.eventLoop, EventLoop)
        self.assertIs(self.eventBuilder, self.eventLoopRunner.eventLoop.eventBuilder)
        self.assertIs(component1, self.eventLoopRunner.eventLoop.component)
        self.assertIs("compName1", self.eventLoopRunner.eventLoop.component.name)
        self.assertEqual([package1.reader, package2.reader], self.eventLoopRunner.eventLoop.readers)

        component2 = MockComponent()
        component2.name = "compName2"
        self.bundle.read(component2)

        self.assertIsInstance(self.eventLoopRunner.eventLoop, EventLoop)
        self.assertIs(self.eventBuilder, self.eventLoopRunner.eventLoop.eventBuilder)
        self.assertIs(component2, self.eventLoopRunner.eventLoop.component)
        self.assertIs("compName2", self.eventLoopRunner.eventLoop.component.name)
        self.assertEqual([package1.reader, package2.reader], self.eventLoopRunner.eventLoop.readers)

        self.assertFalse(self.eventLoopRunner.ended)
        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        self.bundle.end()
        self.assertTrue(self.eventLoopRunner.ended)
        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)

##____________________________________________________________________________||
