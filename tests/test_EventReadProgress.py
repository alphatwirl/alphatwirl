from AlphaTwirl import EventReadProgress
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
