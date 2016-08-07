from AlphaTwirl.Loop import ReaderComposite
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

    def copy_from(self, src):
        self._copy = src

##__________________________________________________________________||
class MockReader_without_copy_from(object):

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
    def copy_from(self, src): pass

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

    def test_copy_from(self):
        """
        composite1
            |- composite2
            |      |- reader1
            |      |- reader2
            |- reader3
            |- reader4 (wo copy_from())
            |- reader5
        """
        dest_composite1 = ReaderComposite()
        dest_composite2 = ReaderComposite()
        dest_reader1 = MockReader()
        dest_reader2 = MockReader()
        dest_reader3 = MockReader()
        dest_reader4 = MockReader_without_copy_from()
        dest_reader5 = MockReader()
        dest_composite1.add(dest_composite2)
        dest_composite2.add(dest_reader1)
        dest_composite2.add(dest_reader2)
        dest_composite1.add(dest_reader3)
        dest_composite1.add(dest_reader4)
        dest_composite1.add(dest_reader5)

        src_composite1 = ReaderComposite()
        src_composite2 = ReaderComposite()
        src_reader1 = MockReader()
        src_reader2 = MockReader()
        src_reader3 = MockReader()
        src_reader4 = MockReader_without_copy_from()
        src_reader5 = MockReader()
        src_composite1.add(src_composite2)
        src_composite2.add(src_reader1)
        src_composite2.add(src_reader2)
        src_composite1.add(src_reader3)
        src_composite1.add(src_reader4)
        src_composite1.add(src_reader5)

        dest_composite1.copy_from(src_composite1)

        self.assertIs(src_reader1, dest_reader1._copy)
        self.assertIs(src_reader2, dest_reader2._copy)
        self.assertIs(src_reader3, dest_reader3._copy)
        self.assertIs(src_reader5, dest_reader5._copy)

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
