from AlphaTwirl.Loop import EventLoop
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class MockEventBuilder(object):
    def __init__(self, events):
        self.events = events

    def build(self, dataset, start, nEvents):
        self.dataset = dataset
        self.start = start
        self.nEvents = nEvents
        return self.events

##__________________________________________________________________||
class MockDataset(object): pass

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

        dataset = MockDataset()

        reader = MockReader()

        obj = EventLoop(eventBuilder, dataset, reader, start = 100, nEvents = 10000)

        self.assertIsNone(reader.beginCalled)
        self.assertFalse(reader.endCalled)
        self.assertEqual([ ], reader.events)

        self.assertEqual(reader, obj())

        self.assertEqual(dataset, eventBuilder.dataset)
        self.assertEqual(100, eventBuilder.start)
        self.assertEqual(10000, eventBuilder.nEvents)

        self.assertIs(events, reader.beginCalled)
        self.assertIsNot(events, reader.events)
        self.assertEqual(events, reader.events)
        self.assertTrue(reader.endCalled)

    def test_call_default_options(self):

        events = [MockEvent(), MockEvent(), MockEvent()]
        eventBuilder = MockEventBuilder(events)

        dataset = MockDataset()

        reader = MockReader()

        obj = EventLoop(eventBuilder, dataset, reader) # don't give start or nEvents

        self.assertIsNone(reader.beginCalled)
        self.assertFalse(reader.endCalled)
        self.assertEqual([ ], reader.events)

        self.assertEqual(reader, obj())

        self.assertEqual(dataset, eventBuilder.dataset)
        self.assertEqual(0, eventBuilder.start) # the default value
        self.assertEqual(-1, eventBuilder.nEvents) # the default value

        self.assertIs(events, reader.beginCalled)
        self.assertIsNot(events, reader.events)
        self.assertEqual(events, reader.events)
        self.assertTrue(reader.endCalled)

##__________________________________________________________________||
