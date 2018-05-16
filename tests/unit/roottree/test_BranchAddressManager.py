import unittest

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.roottree import BranchAddressManager

##__________________________________________________________________||
class MockLeaf(object):
    def __init__(self, name, typename, leafcount = None, maximum = None):
        self.name = name
        self.typename = typename
        self.leafcount = leafcount
        self.maximum = maximum
    def GetName(self): return self.name
    def GetTypeName(self): return self.typename
    def GetLeafCount(self): return self.leafcount
    def GetMaximum(self): return self.maximum

##__________________________________________________________________||
class MockNullLeaf(object):
    def GetName(self): raise ReferenceError('null object')

##__________________________________________________________________||
class MockTree(object):

    def __init__(self, leaves):
        self.leaves = leaves
        self.leafDict = dict([(l.GetName(), l) for l in leaves])
        self.branchstatus = [ ]
        self.branchaddress = [ ]

    def GetListOfLeaves(self):
        return self.leaves

    def GetLeaf(self, name):
        return self.leafDict[name]

    def SetBranchStatus(self, name, status):
        self.branchstatus.append((name, status))

    def SetBranchAddress(self, name, address):
        self.branchaddress.append((name, address))

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestBranchAddressManager(unittest.TestCase):


    def setUp(self):

        run = MockLeaf('run', 'UInt_t', MockNullLeaf())
        lumi = MockLeaf('lumi', 'UInt_t', MockNullLeaf())
        evt  = MockLeaf('evt', 'Int_t', MockNullLeaf())
        met_pt = MockLeaf('met_pt', 'Double_t', MockNullLeaf())
        njet = MockLeaf('njet', 'Int_t', MockNullLeaf(), 13)
        jet_pt = MockLeaf('jet_pt', 'Double_t', njet)
        nele = MockLeaf('nele', 'Int_t', MockNullLeaf(), 0)
        ele_pt = MockLeaf('ele_pt', 'Double_t', nele)
        self.tree1 = MockTree(leaves = [run, lumi, evt, met_pt, njet, jet_pt, nele, ele_pt])

    def tearDown(self):

        BranchAddressManager.arrayDict.clear()
        BranchAddressManager.counterArrayDict.clear()

    def test_getArrays(self):

        manager = BranchAddressManager()

        array_jet_pt, array_jet_pt_count = manager.getArrays(self.tree1, 'jet_pt')
        self.assertEqual('d', array_jet_pt.typecode)
        self.assertEqual(13, array_jet_pt.buffer_info()[1])
        self.assertEqual('i', array_jet_pt_count.typecode)
        self.assertEqual(1, array_jet_pt_count.buffer_info()[1])

    def test_getArrays_same_objects(self):

        manager = BranchAddressManager()

        array_jet_pt_1, array_jet_pt_count_1 = manager.getArrays(self.tree1, 'jet_pt')
        array_jet_pt_2, array_jet_pt_count_2 = manager.getArrays(self.tree1, 'jet_pt')
        self.assertIs(array_jet_pt_1, array_jet_pt_2)
        self.assertIs(array_jet_pt_count_1, array_jet_pt_count_2)

    def test_getArrays_same_objects_different_managers(self):

        manager1 = BranchAddressManager()
        manager2 = BranchAddressManager()

        array_jet_pt_1, array_jet_pt_count_1 = manager1.getArrays(self.tree1, 'jet_pt')
        array_jet_pt_2, array_jet_pt_count_2 = manager2.getArrays(self.tree1, 'jet_pt')
        self.assertIs(array_jet_pt_1, array_jet_pt_2)
        self.assertIs(array_jet_pt_count_1, array_jet_pt_count_2)

    def test_getArrays_no_count(self):

        manager = BranchAddressManager()

        array_met_pt, array_met_pt_count = manager.getArrays(self.tree1, 'met_pt')
        self.assertEqual('d', array_met_pt.typecode)
        self.assertEqual(1, array_met_pt.buffer_info()[1])
        self.assertIsNone(array_met_pt_count)

    def test_getArrays_no_branch(self):

        manager = BranchAddressManager()

        array_zet_pt, array_zet_pt_count = manager.getArrays(self.tree1, 'zet_pt')
        self.assertIsNone(array_zet_pt)
        self.assertIsNone(array_zet_pt_count)

    def test_getArrays_zero_max(self):

        manager = BranchAddressManager()

        array_ele_pt, array_ele_pt_count = manager.getArrays(self.tree1, 'ele_pt')
        self.assertEqual('d', array_ele_pt.typecode)
        self.assertEqual(1, array_ele_pt.buffer_info()[1])
        self.assertEqual('i', array_ele_pt_count.typecode)
        self.assertEqual(1, array_ele_pt_count.buffer_info()[1])

##__________________________________________________________________||
