import sys
import unittest

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.roottree import BranchBuilder

##__________________________________________________________________||
class MockFile(object):
    pass

##__________________________________________________________________||
class MockLeaf(object):
    def __init__(self, name, typename):
        self.name = name
        self.typename = typename

    def GetName(self):
        return self.name

    def GetTypeName(self):
        return self.typename

##__________________________________________________________________||
class MockTree(object):
    def __init__(self, Entries = 100):
        self.Entries = Entries
        self.iEvent = -1
        self.branchstatus = [ ]
        self.getEntryCalled = False
        self.leafNames = ('run', 'evt', 'njet', 'jet_pt', 'met_pt', 'trigger_path', 'EventAuxiliary')
        self.leafTypeNames = ('Int_t', 'Int_t', 'Int_t', 'Double_t', 'Double_t', 'vector<string>', 'edm::EventAuxiliary')
        self.leafs = dict([(n, MockLeaf(n, t)) for n, t in zip(self.leafNames, self.leafTypeNames)])

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

    def GetListOfLeaves(self):
        return self.leafs.values()

    def GetLeaf(self, name):
        return self.leafs[name]

##__________________________________________________________________||
class MockArray(object): pass

##__________________________________________________________________||
class MockBranchAddressManager(object):
    def __init__(self):
        self.leafNames = ('run', 'evt', 'njet', 'jet_pt', 'met_pt')
    def getArrays(self, tree, branchName):
        if branchName in self.leafNames:
            return MockArray(), MockArray()
        return None, None

##__________________________________________________________________||
class MockVector(object): pass

##__________________________________________________________________||
class MockBranchAddressManagerForVector(object):
    def __init__(self):
        self.leafNames = ('trigger_path', )
    def getVector(self, tree, branchName):
        if branchName in self.leafNames:
            return MockVector()
        return None

##__________________________________________________________________||
class MockBranch(object):
    def __init__(self, name, array, countarray):
        pass

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
class TestBranchBuilder(unittest.TestCase):

    def setUp(self):
        self.moduleBranchBuilder = sys.modules['alphatwirl.roottree.BranchBuilder']
        self.org_branchAddressManager = self.moduleBranchBuilder.branchAddressManager
        self.moduleBranchBuilder.branchAddressManager = MockBranchAddressManager()

        self.org_branchAddressManagerForVector = self.moduleBranchBuilder.branchAddressManagerForVector
        self.moduleBranchBuilder.branchAddressManagerForVector = MockBranchAddressManagerForVector()

        self.org_Branch = self.moduleBranchBuilder.Branch
        self.moduleBranchBuilder.Branch = MockBranch

    def tearDown(self):
        self.moduleBranchBuilder.branchAddressManager = self.org_branchAddressManager
        self.moduleBranchBuilder.branchAddressManagerForVector = self.org_branchAddressManagerForVector
        self.moduleBranchBuilder.Branch = self.org_Branch
        BranchBuilder.itsdict.clear()

    def test_init(self):
        builder = BranchBuilder()

    def test_repr(self):
        builder = BranchBuilder()
        repr(builder)

    def test_getattr(self):
        builder = BranchBuilder()
        tree = MockTree()

        jet_pt = builder(tree, "jet_pt")
        met_pt = builder(tree, "met_pt")
        self.assertIsInstance(jet_pt, MockBranch)
        self.assertIsInstance(met_pt, MockBranch)

    def test_getattr_same_objects_different_calls(self):

        builder = BranchBuilder()

        tree = MockTree()
        jet_pt1 = builder(tree, "jet_pt")
        met_pt1 = builder(tree, "met_pt")

        jet_pt2 = builder(tree, "jet_pt")
        met_pt2 = builder(tree, "met_pt")

        self.assertIs(jet_pt1, jet_pt2)
        self.assertIs(met_pt1, met_pt2)

    def test_getattr_same_objects_different_builders(self):

        builder1 = BranchBuilder()
        builder2 = BranchBuilder()

        tree = MockTree()
        jet_pt1 = builder1(tree, "jet_pt")
        met_pt1 = builder1(tree, "met_pt")

        jet_pt2 = builder2(tree, "jet_pt")
        met_pt2 = builder2(tree, "met_pt")

        self.assertIs(jet_pt1, jet_pt2)
        self.assertIs(met_pt1, met_pt2)

    def test_getattr_None(self):
        builder = BranchBuilder()

        tree = MockTree()

        self.assertIsNone(builder(tree, 'no_such_branch'))

    @unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
    def test_getattr_warning(self):
        builder = BranchBuilder()

        tree = MockTree()

        self.assertIsNone(builder(tree, 'EventAuxiliary'))

    def test_register_tree(self):
        builder = BranchBuilder()

        tree = MockTree()

        builder.register_tree(tree)

        self.assertEqual([('*', 0)], tree.branchstatus)

##__________________________________________________________________||
