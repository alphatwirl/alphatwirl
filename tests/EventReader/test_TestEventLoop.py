from AlphaTwirl.EventReader import EventLoop
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    def __init__(self, id):
        self.id = id

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

##____________________________________________________________________________||
class TestEventLoop(unittest.TestCase):

    def test_call(self):
        eventBuilder = MockEventBuilder()
        component = MockComponent()
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        component._events = [event1, event2, event3]

        reader1 = MockReader()
        reader2 = MockReader()
        readers = [reader1, reader2]

        loop = EventLoop(eventBuilder, component, readers)

        self.assertEqual(readers, loop())
        self.assertEqual([101, 102, 103], reader1._eventIds)
        self.assertEqual([101, 102, 103], reader2._eventIds)

##____________________________________________________________________________||
