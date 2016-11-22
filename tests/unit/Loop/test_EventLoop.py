from AlphaTwirl.Loop import EventLoop
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class MockEventBuilder(object):
    def __init__(self, events):
        self.events = events

    def build(self, chunk):
        self.chunk = chunk
        return self.events

##__________________________________________________________________||
class MockChunk(object): pass

##__________________________________________________________________||
class MockReader(object):
    def __init__(self):
        self.events = [ ]
        self.beginCalled = None
        self.endCalled = False

    def begin(self, event):
        self.beginCalled = event

    def event(self, event):
        self.events.append(event)

    def end(self):
        self.endCalled = True

##__________________________________________________________________||
class TestEventLoop(unittest.TestCase):

    def test_call(self):

        events = [MockEvent(), MockEvent(), MockEvent()]
        eventBuilder = MockEventBuilder(events)

        chunk = MockChunk()

        reader = MockReader()

        obj = EventLoop(eventBuilder, chunk, reader)

        self.assertIsNone(reader.beginCalled)
        self.assertFalse(reader.endCalled)
        self.assertEqual([ ], reader.events)

        self.assertEqual(reader, obj())

        self.assertEqual(chunk, eventBuilder.chunk)

        self.assertIs(events, reader.beginCalled)
        self.assertIsNot(events, reader.events)
        self.assertEqual(events, reader.events)
        self.assertTrue(reader.endCalled)

##__________________________________________________________________||
