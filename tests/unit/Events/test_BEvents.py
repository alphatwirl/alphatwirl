import sys
import unittest

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    from AlphaTwirl.Events import BEvents
    hasROOT = True
except ImportError:
    pass

##__________________________________________________________________||
class MockFile(object): pass

##__________________________________________________________________||
class MockTree(object):
    def __init__(self, Entries = 100):
        self.Entries = Entries
        self.iEvent = -1
        self.branchstatus = [ ]
        self.getEntryCalled = False
        self.directory = MockFile()
    def GetDirectory(self):
        return self.directory
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

##__________________________________________________________________||
class MockBranch(object): pass

##__________________________________________________________________||
class MockBranchBuilder(object):
    def __init__(self):
        self.next = None
    def __call__(self, tree, name):
        return self.next

##__________________________________________________________________||
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

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestBEvents(unittest.TestCase):

    def test_init_branch_status(self):
        tree = MockTree()
        self.assertEqual([ ], tree.branchstatus)
        events = BEvents(tree)
        events.buildBranch = MockBranchBuilder()
        self.assertEqual([('*', 0)], tree.branchstatus)

    def test_getattr(self):
        tree = MockTree()
        events = BEvents(tree)
        branchBuilder = MockBranchBuilder()
        events.buildBranch = branchBuilder

        branchBuilder.next = MockBranch()
        jet_pt = events.jet_pt
        self.assertIsInstance(jet_pt, MockBranch)

    def test_getattr_same_objects(self):
        tree = MockTree()
        events = BEvents(tree)
        branchBuilder = MockBranchBuilder()
        events.buildBranch = branchBuilder

        branch1 = MockBranch()
        branchBuilder.next = branch1
        jet_pt1 = events.jet_pt
        self.assertIs(branch1, jet_pt1)

        branch2 = MockBranch()
        branchBuilder.next = branch2
        jet_pt2 = events.jet_pt

        self.assertIs(branch1, jet_pt2)
        self.assertIsNot(branch2, jet_pt2)

        it = iter(events)
        event = next(it)

        branch3 = MockBranch()
        branchBuilder.next = branch3
        jet_pt3 = event.jet_pt

        self.assertIs(branch1, jet_pt3)
        self.assertIsNot(branch3, jet_pt3)

    def test_getattr_exception(self):
        tree = MockTree()
        events = BEvents(tree)
        events.buildBranch = MockBranchBuilder()

        self.assertRaises(AttributeError, events.__getattr__, 'no_such_branch')

    def test_getattr_getentry(self):
        tree = MockTree()
        events = BEvents(tree, start = 10)
        branchBuilder = MockBranchBuilder()
        events.buildBranch = branchBuilder

        self.assertEqual(-1, events.iEvent)
        self.assertEqual(-1, tree.iEvent)
        self.assertFalse(tree.getEntryCalled)
        branchBuilder.next = MockBranch()
        jet_pt = events.jet_pt
        self.assertFalse(tree.getEntryCalled)

        it = iter(events)
        event = next(it)
        tree.getEntryCalled = False
        self.assertEqual(0, events.iEvent)
        self.assertEqual(10, tree.iEvent)
        self.assertFalse(tree.getEntryCalled)
        jet_pt = event.jet_pt
        self.assertFalse(tree.getEntryCalled)

        tree.getEntryCalled = False
        met_pt = event.met_pt
        self.assertTrue(tree.getEntryCalled)
        self.assertEqual(0, events.iEvent)
        self.assertEqual(10, tree.iEvent)

    def test_pass_arguments_to_base_class(self):
        tree = MockTree(Entries = 1000)
        events = BEvents(tree, 100)
        self.assertEqual(100, events.nEvents)
        self.assertEqual(0, events.start)

        events = BEvents(tree, 100, 20)
        self.assertEqual(100, events.nEvents)
        self.assertEqual(20, events.start)


##__________________________________________________________________||
