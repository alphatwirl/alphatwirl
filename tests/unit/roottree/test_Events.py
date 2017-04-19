import unittest

from alphatwirl.roottree import Events

##__________________________________________________________________||
class MockFile(object):
    pass

##__________________________________________________________________||
class MockTree(object):
    def __init__(self, entries = 100):
        self.entries = entries
        self.ievent = -1
        self.branch1 = 1111
        self.directory = MockFile()
    def GetDirectory(self):
        return self.directory
    def GetEntries(self):
        return self.entries
    def GetEntry(self, ientry):
        if ientry < self.entries:
            nbytes = 10
            self.ievent = ientry
        else:
            nbytes = 0
            self.ievent = -1
        return nbytes

##__________________________________________________________________||
class TestMockTree(unittest.TestCase):

    def test_mocktree(self):
        tree = MockTree(entries = 3)
        self.assertIsInstance(tree.GetDirectory(), MockFile)
        self.assertEqual(3, tree.GetEntries())

        self.assertEqual(-1, tree.ievent)

        nbytes = 10
        self.assertEqual(nbytes, tree.GetEntry(0))
        self.assertEqual(0, tree.ievent)
        self.assertEqual(nbytes, tree.GetEntry(1))
        self.assertEqual(1, tree.ievent)
        self.assertEqual(nbytes, tree.GetEntry(2))
        self.assertEqual(2, tree.ievent)
        self.assertEqual(0, tree.GetEntry(3))
        self.assertEqual(-1, tree.ievent)

##__________________________________________________________________||
class TestEvents(unittest.TestCase):

    def setUp(self):
        self.tree = MockTree()
        self.events = Events(self.tree)

    def test_init(self):
        tree = MockTree()
        events = Events(tree)
        events = Events(tree, 100)

        self.assertIs(tree, events.tree)

    def test_repr(self):
        repr(self.events)

    def test_nEvents(self):
        tree = MockTree(entries = 100)
        events = Events(tree)
        self.assertEqual(100, events.nEvents) # default the same as entries

        events = Events(tree, -1)
        self.assertEqual(100, events.nEvents) # the same as entries

        events = Events(tree, 50)
        self.assertEqual(50, events.nEvents)

        events = Events(tree, 120)
        self.assertEqual(100, events.nEvents)

        events = Events(tree, 100)
        self.assertEqual(100, events.nEvents)

    def test_nEvents_start(self):

        tree = MockTree(entries = 100)

        events = Events(tree, maxEvents = -1, start = 1)
        self.assertEqual(99, events.nEvents)

        events = Events(tree, maxEvents = 10, start = 1)
        self.assertEqual(10, events.nEvents)

        events = Events(tree, maxEvents = -1, start = 99)
        self.assertEqual(1, events.nEvents)

        events = Events(tree, maxEvents = 20, start = 99)
        self.assertEqual(1, events.nEvents)

        events = Events(tree, maxEvents = -1, start = 100)
        self.assertEqual(0, events.nEvents)

        events = Events(tree, maxEvents = -1, start = 110)
        self.assertEqual(0, events.nEvents)

        events = Events(tree, maxEvents = 10, start = 110)
        self.assertEqual(0, events.nEvents)

        self.assertRaises(ValueError, Events, tree, maxEvents = -1, start = -10)

    def test_iter_iEvent(self):
        tree = MockTree(entries = 4)
        events = Events(tree)
        self.assertEqual(-1, events.iEvent)

        it = iter(events)
        event = next(it)
        self.assertEqual(0, event.iEvent)
        self.assertEqual(0, tree.ievent)
        event = next(it)
        self.assertEqual(1, event.iEvent)
        self.assertEqual(1, tree.ievent)
        event = next(it)
        self.assertEqual(2, event.iEvent)
        self.assertEqual(2, tree.ievent)
        event = next(it)
        self.assertEqual(3, event.iEvent)
        self.assertEqual(3, tree.ievent)
        self.assertRaises(StopIteration, next, it)
        self.assertEqual(-1, event.iEvent)

    def test_iter_maxEvents(self):
        tree = MockTree(entries = 40)
        events = Events(tree, maxEvents = 4)
        self.assertEqual(-1, events.iEvent)

        it = iter(events)
        event = next(it)
        self.assertEqual(0, event.iEvent)
        event = next(it)
        self.assertEqual(1, event.iEvent)
        event = next(it)
        self.assertEqual(2, event.iEvent)
        event = next(it)
        self.assertEqual(3, event.iEvent)
        self.assertRaises(StopIteration, next, it)
        self.assertEqual(-1, event.iEvent)

    def test_iter_iEvent_start(self):
        tree = MockTree(entries = 4)
        events = Events(tree, start = 2)
        self.assertEqual(-1, events.iEvent)

        it = iter(events)
        event = next(it)
        self.assertEqual(0, event.iEvent)
        self.assertEqual(2, tree.ievent)
        event = next(it)
        self.assertEqual(1, event.iEvent)
        self.assertEqual(3, tree.ievent)
        self.assertRaises(StopIteration, next, it)
        self.assertEqual(-1, event.iEvent)

    def test_iter_maxEvents_start(self):
        tree = MockTree(entries = 40)
        events = Events(tree, maxEvents = 4, start = 2)
        self.assertEqual(-1, events.iEvent)

        it = iter(events)
        event = next(it)
        self.assertEqual(0, event.iEvent)
        self.assertEqual(2, tree.ievent)
        event = next(it)
        self.assertEqual(1, event.iEvent)
        self.assertEqual(3, tree.ievent)
        event = next(it)
        self.assertEqual(2, event.iEvent)
        self.assertEqual(4, tree.ievent)
        event = next(it)
        self.assertEqual(3, event.iEvent)
        self.assertEqual(5, tree.ievent)
        self.assertRaises(StopIteration, next, it)
        self.assertEqual(-1, event.iEvent)

    def test_iter_getattr(self):
        tree = MockTree(entries = 5)
        events = Events(tree)
        it = iter(events)
        event = next(it)
        self.assertEqual(1111, event.branch1)
        tree.branch1 = 2222
        self.assertEqual(2222, event.branch1)

    def test_getitem(self):
        tree = MockTree(entries = 4)
        events = Events(tree)
        self.assertEqual(-1, events.iEvent)

        event = events[0]
        self.assertEqual(0, event.iEvent)
        self.assertEqual(0, tree.ievent)
        event = events[1]
        self.assertEqual(1, event.iEvent)
        self.assertEqual(1, tree.ievent)
        event = events[2]
        self.assertEqual(2, event.iEvent)
        self.assertEqual(2, tree.ievent)
        event = events[3]
        self.assertEqual(3, event.iEvent)
        self.assertEqual(3, tree.ievent)
        self.assertRaises(IndexError, events.__getitem__, 4)
        self.assertEqual(-1, events.iEvent)

    def test_getitem_start(self):
        tree = MockTree(entries = 4)
        events = Events(tree, start = 2)
        self.assertEqual(-1, events.iEvent)

        event = events[0]
        self.assertEqual(0, event.iEvent)
        self.assertEqual(2, tree.ievent)
        event = events[1]
        self.assertEqual(1, event.iEvent)
        self.assertEqual(3, tree.ievent)
        self.assertRaises(IndexError, events.__getitem__, 4)
        self.assertEqual(-1, events.iEvent)

##__________________________________________________________________||
