from AlphaTwirl.Events import Events
import unittest

##____________________________________________________________________________||
class MockFile(object):
    pass

##____________________________________________________________________________||
class MockTree(object):
    def __init__(self, Entries = 100):
        self.Entries = Entries
        self.iEvent = -1
        self.branch1 = 1111
    def GetDirectory(self):
        return MockFile()
    def GetEntries(self):
        return self.Entries
    def GetEntry(self, ientry):
        if ientry < self.Entries:
            nbytes = 10
            self.iEvent = ientry
        else:
            nbytes = 0
            self.iEvent = -1
        return nbytes

##____________________________________________________________________________||
class TestMockTree(unittest.TestCase):

    def test_mocktree(self):
        tree = MockTree(Entries = 3)
        self.assertIsInstance(tree.GetDirectory(), MockFile)
        self.assertEqual(3, tree.GetEntries())

        self.assertEqual(-1, tree.iEvent)

        nbytes = 10
        self.assertEqual(nbytes, tree.GetEntry(0))
        self.assertEqual(0, tree.iEvent)
        self.assertEqual(nbytes, tree.GetEntry(1))
        self.assertEqual(1, tree.iEvent)
        self.assertEqual(nbytes, tree.GetEntry(2))
        self.assertEqual(2, tree.iEvent)
        self.assertEqual(0, tree.GetEntry(3))
        self.assertEqual(-1, tree.iEvent)

##____________________________________________________________________________||
class TestEvents(unittest.TestCase):

    def setUp(self):
        self.tree = MockTree()
        self.events = Events(self.tree)

    def test_init(self):
        tree = MockTree()
        events = Events(tree)
        events = Events(tree, 100)

        self.assertIs(tree, events.tree)

    def test_nEvents(self):
        tree = MockTree(Entries = 100)
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

    def test_iter_iEvent(self):
        tree = MockTree(Entries = 4)
        events = Events(tree)
        self.assertEqual(-1, events.iEvent)

        it = iter(events)
        event = next(it)
        self.assertEqual(0, event.iEvent)
        self.assertEqual(0, tree.iEvent)
        event = next(it)
        self.assertEqual(1, event.iEvent)
        self.assertEqual(1, tree.iEvent)
        event = next(it)
        self.assertEqual(2, event.iEvent)
        self.assertEqual(2, tree.iEvent)
        event = next(it)
        self.assertEqual(3, event.iEvent)
        self.assertEqual(3, tree.iEvent)
        self.assertRaises(StopIteration, next, it)
        self.assertEqual(-1, event.iEvent)

    def test_iter_maxEvents(self):
        tree = MockTree(Entries = 40)
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

    def test_iter_getattr(self):
        tree = MockTree(Entries = 5)
        events = Events(tree)
        it = iter(events)
        event = next(it)
        self.assertEqual(1111, event.branch1)
        tree.branch1 = 2222
        self.assertEqual(2222, event.branch1)

##____________________________________________________________________________||
