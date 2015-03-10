from AlphaTwirl import EventReadProgress, EventReadProgressBuilder, EventReadProgressB, EventReadProgressBBuilder
import unittest
import cStringIO


##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class TestEventReadProgress(unittest.TestCase):

    def test_init(self):
        out = cStringIO.StringIO()
        progress = EventReadProgress(1000, out = out)

    def test_event(self):
        progress = EventReadProgress(1000)
        event = MockEvent()
        event.nEvents = 124344

        event.iEvent = 0
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('', progress.out.getvalue())

        event.iEvent = 999
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('  1000 / 124344\n', progress.out.getvalue())

        event.iEvent = 1999
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('  2000 / 124344\n', progress.out.getvalue())

        event.iEvent = 2000
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('', progress.out.getvalue())

        event.iEvent = 124343
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('124344 / 124344\n', progress.out.getvalue())

##____________________________________________________________________________||
class TestEventReadProgressBuilder(unittest.TestCase):
    def test_call(self):
        out = cStringIO.StringIO()
        builder = EventReadProgressBuilder(2345, out)
        progress1 = builder()
        progress2 = builder()
        self.assertIsInstance(progress1, EventReadProgress)
        self.assertIsInstance(progress2, EventReadProgress)
        self.assertIsNot(progress1, progress2)
        self.assertIs(out, progress1.out)
        self.assertIs(out, progress2.out)
        self.assertIs(2345, progress1.pernevents)
        self.assertIs(2345, progress2.pernevents)

##____________________________________________________________________________||
class TestEventReadProgressB(unittest.TestCase):

    def test_init(self):
        out = cStringIO.StringIO()
        progress = EventReadProgressB(1000, out = out)

    def test_event(self):
        progress = EventReadProgressB(1000)
        event = MockEvent()
        event.nEvents = 124344

        event.iEvent = 0
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('     1 / 124344', progress.out.getvalue())

        event.iEvent = 999
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08  1000 / 124344', progress.out.getvalue())

        event.iEvent = 1999
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08  2000 / 124344', progress.out.getvalue())

        event.iEvent = 2000
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('', progress.out.getvalue())

        event.iEvent = 124343
        progress.out = cStringIO.StringIO()
        progress.event(event)
        self.assertEqual('\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08124344 / 124344\n', progress.out.getvalue())

##____________________________________________________________________________||
class TestEventReadProgressBuilder(unittest.TestCase):
    def test_call(self):
        out = cStringIO.StringIO()
        builder = EventReadProgressBBuilder(2345, out)
        progress1 = builder()
        progress2 = builder()
        self.assertIsInstance(progress1, EventReadProgressB)
        self.assertIsInstance(progress2, EventReadProgressB)
        self.assertIsNot(progress1, progress2)
        self.assertIs(out, progress1.out)
        self.assertIs(out, progress2.out)
        self.assertIs(2345, progress1.pernevents)
        self.assertIs(2345, progress2.pernevents)

##____________________________________________________________________________||
