from alphatwirl.loop import EventLoop
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class MockEventBuilder(object):
    def __init__(self, events):
        self.events = events

    def __call__(self):
        return self.events

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

        event1 = MockEvent()
        event2 = MockEvent()
        event3 = MockEvent()
        events = [event1, event2, event3]
        build_events = MockEventBuilder(events)

        reader = MockReader()

        obj = EventLoop(build_events, reader)

        self.assertIsNone(reader.beginCalled)
        self.assertFalse(reader.endCalled)
        self.assertEqual([ ], reader.events)

        self.assertEqual(reader, obj())

        self.assertEqual([event1, event2, event3], reader.events)

        self.assertIs(events, reader.beginCalled)
        self.assertIsNot(events, reader.events)
        self.assertEqual(events, reader.events)
        self.assertTrue(reader.endCalled)

##__________________________________________________________________||
