from AlphaTwirl.EventReader import ReaderWithEventSelection
import unittest

##__________________________________________________________________||
class MockReader(object):

    def __init__(self):
        self._beganWith = None
        self._events = [ ]
        self._ended = False
        self._copy = None

    def begin(self, event):
        self._beganWith = event

    def event(self, event):
        self._events.append(event)

    def end(self):
        self._ended = True

    def copyFrom(self, src):
        self._copy = src

##__________________________________________________________________||
class MockEventSelection(object):
    def __init__(self, toSelect):
        self.toSelect = toSelect

    def __call__(self, event):
        return event.id in self.toSelect

##__________________________________________________________________||
class MockEvent(object):
    def __init__(self, id):
        self.id = id

##__________________________________________________________________||
class TestReaderWithEventSelection(unittest.TestCase):

    def test_one(self):
        reader = MockReader()
        eventSelection = MockEventSelection((102, 104, 105))
        rws = ReaderWithEventSelection(reader, eventSelection)

        events = MockEvent(0)
        rws.begin(events)
        self.assertIs(events, reader._beganWith)

        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        event4 = MockEvent(104)
        event5 = MockEvent(105)
        rws.event(event1)
        rws.event(event2)
        rws.event(event3)
        rws.event(event4)
        rws.event(event5)

        self.assertEqual([event2, event4, event5], reader._events)

        rws.end()
        self.assertTrue(reader._ended)

    def test_copyFrom(self):
        reader = MockReader()
        eventSelection = MockEventSelection((102, 104, 105))
        rws = ReaderWithEventSelection(reader, eventSelection)

        src_reader = MockReader()
        src_rws = ReaderWithEventSelection(src_reader, eventSelection)

        self.assertIsNone(reader._copy)
        rws.copyFrom(src_rws)
        self.assertIs(src_reader, reader._copy)

##__________________________________________________________________||
