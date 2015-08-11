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
    def build(self, dataset):
        return dataset._events

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
class MockDataset(object):
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
        dataset = MockDataset()
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        event4 = MockEvent(104)
        event5 = MockEvent(105)
        events = [event1, event2, event3, event4, event5]
        dataset._events = events

        reader = MockReader()

        loop = EventLoop(eventBuilder, eventSelection, dataset, reader)

        self.assertFalse(reader._begin)
        self.assertEqual([ ], reader._eventIds)
        self.assertFalse(reader._end)

        self.assertEqual(reader, loop())

        self.assertEqual(events, reader._begin)
        self.assertEqual([102, 104, 105], reader._eventIds)
        self.assertTrue(reader._end)

##____________________________________________________________________________||
