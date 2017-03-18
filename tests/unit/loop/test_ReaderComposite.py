from alphatwirl.loop import ReaderComposite
import unittest

##__________________________________________________________________||
class MockReader(object):

    def __init__(self):
        self._beganWith = None
        self._events = [ ]
        self._ended = False

    def begin(self, event):
        self._beganWith = event

    def event(self, event):
        self._events.append(event)

    def end(self):
        self._ended = True

##__________________________________________________________________||
class MockReader_without_begin_end(object):

    def __init__(self):
        self._events = [ ]

    def event(self, event):
        self._events.append(event)

##__________________________________________________________________||
class MockReader_with_return(object):
    def __init__(self):
        self._events = [ ]
        self._ret = None

    def begin(self, event): pass

    def event(self, event):
        self._events.append(event)
        return self._ret

    def end(self): pass

##__________________________________________________________________||
class MockEvent(object):
    pass

##__________________________________________________________________||
class TestReaderComposite(unittest.TestCase):

    def test_event_two_readers_two_events(self):
        """
        composite
            |- reader1
            |- reader2
        """
        composite = ReaderComposite()
        reader1 = MockReader()
        reader2 = MockReader()
        composite.add(reader1)
        composite.add(reader2)

        events = MockEvent()
        composite.begin(events)
        self.assertIs(events, reader1._beganWith)
        self.assertIs(events, reader2._beganWith)

        event1 = MockEvent()
        composite.event(event1)

        event2 = MockEvent()
        composite.event(event2)
        self.assertEqual([event1, event2], reader1._events)
        self.assertEqual([event1, event2], reader2._events)

        composite.end()
        self.assertTrue(reader1._ended)
        self.assertTrue(reader2._ended)

    def test_event_nested_composite(self):
        """
        composite1
            |- composite2
            |      |- reader1
            |      |- reader2
            |- reader3
        """
        composite1 = ReaderComposite()
        composite2 = ReaderComposite()
        reader1 = MockReader()
        reader2 = MockReader()
        reader3 = MockReader()
        composite1.add(composite2)
        composite2.add(reader1)
        composite2.add(reader2)
        composite1.add(reader3)

        events = MockEvent()
        composite1.begin(events)
        self.assertIs(events, reader1._beganWith)
        self.assertIs(events, reader2._beganWith)
        self.assertIs(events, reader3._beganWith)

        event1 = MockEvent()
        composite1.event(event1)

        event2 = MockEvent()
        composite1.event(event2)
        self.assertEqual([event1, event2], reader1._events)
        self.assertEqual([event1, event2], reader2._events)
        self.assertEqual([event1, event2], reader3._events)

        composite1.end()
        self.assertTrue(reader1._ended)
        self.assertTrue(reader2._ended)
        self.assertTrue(reader3._ended)

    def test_return_False(self):
        """
        composite
            |- reader1 (return None)
            |- reader2 (return True)
            |- reader3 (return False)
            |- reader4
        """
        composite = ReaderComposite()
        reader1 = MockReader_with_return()
        reader2 = MockReader_with_return()
        reader3 = MockReader_with_return()
        reader4 = MockReader_with_return()
        composite.add(reader1)
        composite.add(reader2)
        composite.add(reader3)
        composite.add(reader4)

        events = MockEvent()
        composite.begin(events)

        reader1._ret = None
        reader2._ret = True
        reader3._ret = False

        event1 = MockEvent()
        ret = composite.event(event1)

        self.assertEqual([event1, ], reader1._events)
        self.assertEqual([event1, ], reader2._events)
        self.assertEqual([event1, ], reader3._events)
        self.assertEqual([ ], reader4._events)
        self.assertIsNone(ret)

        composite.end()

    def test_no_begin_end(self):
        """
        composite
            |- reader1
            |- reader2 (without begin end)
            |- reader3
        """
        composite = ReaderComposite()
        reader1 = MockReader()
        reader2 = MockReader_without_begin_end()
        reader3 = MockReader()
        composite.add(reader1)
        composite.add(reader2)
        composite.add(reader3)

        events = MockEvent()
        composite.begin(events)
        self.assertIs(events, reader1._beganWith)

        event1 = MockEvent()
        composite.event(event1)

        event2 = MockEvent()
        composite.event(event2)
        self.assertEqual([event1, event2], reader1._events)
        self.assertEqual([event1, event2], reader2._events)
        self.assertEqual([event1, event2], reader3._events)

        composite.end()
        self.assertTrue(reader1._ended)
        self.assertTrue(reader3._ended)

##__________________________________________________________________||
