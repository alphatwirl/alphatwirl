from AlphaTwirl.Events import BEvents
from AlphaTwirl.Events import Branch
import sys
import unittest

##____________________________________________________________________________||
class MockFile(object):
    pass

##____________________________________________________________________________||
class MockTree(object):
    def __init__(self, Entries = 100):
        self.Entries = Entries
        self.iEvent = -1
        self.leafNames = ('run', 'evt', 'njet', 'jet_pt', 'met_pt')
        self.branchstatus = [ ]
        self.getEntryCalled = False
    def GetDirectory(self):
        return MockFile()
    def GetEntries(self):
        return self.Entries
    def GetEntry(self, ientry):
        self.getEntryCalled = True
        if ientry < self.Entries:
            nbytes = 10
            self.iEvent = ientry
        else:
            nbytes = 0
            self.iEvent = -1
        return nbytes

    def SetBranchStatus(self, bname, status):
        self.branchstatus.append((bname, status))

    def _isleafName(self, name): return name in self.leafNames


##____________________________________________________________________________||
class MockArray(object): pass

##____________________________________________________________________________||
class MockBranchAddressManager(object):
    def getArrays(self, tree, branchName):
        if tree._isleafName(branchName):
            return MockArray(), MockArray()
        return None, None

##____________________________________________________________________________||
class MockBranch(object):
    def __init__(self, name, array, countarray):
        pass

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
class TestBEvents(unittest.TestCase):

    def setUp(self):
        self.moduleBEvents = sys.modules['AlphaTwirl.Events.BEvents']
        self.org_branchAddressManager = self.moduleBEvents.branchAddressManager
        self.moduleBEvents.branchAddressManager = MockBranchAddressManager()

        self.org_Branch = self.moduleBEvents.Branch
        self.moduleBEvents.Branch = MockBranch

    def tearDown(self):
        self.moduleBEvents.branchAddressManager = self.org_branchAddressManager
        self.moduleBEvents.Branch = self.org_Branch

    def test_init(self):
        tree = MockTree()
        self.assertEqual([ ], tree.branchstatus)
        events = BEvents(tree)
        self.assertEqual([('*', 0)], tree.branchstatus)

    def test_getattr(self):
        tree = MockTree()
        events = BEvents(tree)

        jet_pt = events.jet_pt
        met_pt = events.met_pt
        self.assertIsInstance(jet_pt, MockBranch)
        self.assertIsInstance(met_pt, MockBranch)

    def test_getattr_same_objects(self):
        tree = MockTree()
        events = BEvents(tree)

        jet_pt1 = events.jet_pt
        met_pt1 = events.met_pt

        jet_pt2 = events.jet_pt
        met_pt2 = events.met_pt

        self.assertIs(jet_pt1, jet_pt2)
        self.assertIs(met_pt1, met_pt2)

        it = iter(events)
        event = next(it)

        jet_pt3 = event.jet_pt
        met_pt3 = event.met_pt

        self.assertIs(jet_pt1, jet_pt3)
        self.assertIs(met_pt1, met_pt3)

    def test_getattr_exception(self):
        tree = MockTree()
        events = BEvents(tree)

        self.assertRaises(AttributeError, events.__getattr__, 'no_such_branch')

    def test_getattr_getentry(self):
        tree = MockTree()
        events = BEvents(tree)

        self.assertEqual(-1, events.iEvent)
        self.assertFalse(tree.getEntryCalled)
        jet_pt = events.jet_pt
        self.assertFalse(tree.getEntryCalled)

        it = iter(events)
        event = next(it)
        tree.getEntryCalled = False
        self.assertEqual(0, events.iEvent)
        self.assertFalse(tree.getEntryCalled)
        jet_pt = event.jet_pt
        self.assertFalse(tree.getEntryCalled)

        met_pt = event.met_pt
        self.assertTrue(tree.getEntryCalled)

##____________________________________________________________________________||
