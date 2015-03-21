from AlphaTwirl.EventReader import EventLoop
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    def __init__(self, id):
        self.id = id
        self.iEvent = 0
        self.nEvents = 0

##____________________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self):
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self):
        self._events = None
        self.name = None

##____________________________________________________________________________||
class MockEventSelection(object):
    def __init__(self, toSelect):
        self.toSelect = toSelect

    def __call__(self, event):
        return event.id in self.toSelect

##____________________________________________________________________________||
class TestEventLoop(unittest.TestCase):

    def test_call(self):
        eventBuilder = MockEventBuilder()
        eventSelection = MockEventSelection((102, 104, 105))
        component = MockComponent()
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        event4 = MockEvent(104)
        event5 = MockEvent(105)
        component._events = [event1, event2, event3, event4, event5]

        reader1 = MockReader()
        reader2 = MockReader()
        readers = [reader1, reader2]

        loop = EventLoop(eventBuilder, eventSelection, component, readers)

        self.assertEqual(readers, loop())
        self.assertEqual([102, 104, 105], reader1._eventIds)
        self.assertEqual([102, 104, 105], reader2._eventIds)

##____________________________________________________________________________||
