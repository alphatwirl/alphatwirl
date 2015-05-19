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
        self._begin = False
        self._end = False

    def begin(self, event):
        self._begin = event

    def event(self, event):
        self._eventIds.append(event.id)

    def end(self):
        self._end = True

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
        events = [event1, event2, event3, event4, event5]
        component._events = events

        reader1 = MockReader()
        reader2 = MockReader()
        readers = [reader1, reader2]

        loop = EventLoop(eventBuilder, eventSelection, component, readers)

        self.assertFalse(reader1._begin)
        self.assertFalse(reader2._begin)
        self.assertEqual([ ], reader1._eventIds)
        self.assertEqual([ ], reader2._eventIds)
        self.assertFalse(reader1._end)
        self.assertFalse(reader2._end)

        self.assertEqual(readers, loop())

        self.assertEqual(events, reader1._begin)
        self.assertEqual(events, reader2._begin)
        self.assertEqual([102, 104, 105], reader1._eventIds)
        self.assertEqual([102, 104, 105], reader2._eventIds)
        self.assertTrue(reader1._end)
        self.assertTrue(reader2._end)

##____________________________________________________________________________||
