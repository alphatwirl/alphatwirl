import unittest
import os
import sys

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.roottree import BEvents as Events
    from alphatwirl.roottree import Branch

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
# @unittest.skip("skip TestBEventsWithFile")
class TestBEventsWithFileBranch(unittest.TestCase):

    def setUp(self):
        inputFile = 'sample_01.root'
        treeName = 'tree'
        inputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), inputFile)

        self.inputFile = ROOT.TFile.Open(inputPath)
        self.tree = self.inputFile.Get(treeName)
        self.events = Events(self.tree)

    def tearDown(self):
        pass

    def test_branch(self):
        jet_pt = self.events.jet_pt
        met_pt = self.events.met_pt
        self.assertIsInstance(jet_pt, Branch)
        self.assertIsInstance(met_pt, Branch)

        self.assertEqual(0, len(jet_pt))
        self.assertEqual(1, len(met_pt))
        self.assertEqual(0.0, met_pt[0])

        self._assert_contents(jet_pt, met_pt)
        self._assert_contents(jet_pt, met_pt) # assert twice

    def test_2_events(self):
        jet_pt = self.events.jet_pt
        met_pt = self.events.met_pt
        self._assert_contents(jet_pt, met_pt)

        # the 2nd events object from the same tree
        events2 = Events(self.tree)
        jet_pt2 = events2.jet_pt
        met_pt2 = events2.met_pt
        self.assertIs(jet_pt, jet_pt2)
        self.assertIs(met_pt, met_pt2)
        self._assert_contents(jet_pt, met_pt)

    def _assert_contents(self, jet_pt, met_pt):

        self.tree.GetEntry(0)
        self.assertEqual(2, len(jet_pt))
        self.assertEqual(1, len(met_pt))
        self.assertEqual(124.55626678466797, jet_pt[0])
        self.assertEqual(86.90544128417969, jet_pt[1])
        self.assertAlmostEqual(43.783382415771484, met_pt[0])

        self.tree.GetEntry(1)
        self.assertEqual(3, len(jet_pt))
        self.assertEqual(1, len(met_pt))
        self.assertEqual(112.48554992675781, jet_pt[0])
        self.assertEqual(52.32780075073242, jet_pt[1])
        self.assertEqual(48.861289978027344, jet_pt[2])
        self.assertAlmostEqual(20.483951568603516, met_pt[0])

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
# @unittest.skip("skip TestBEventsWithFile")
class TestBEventsWithFileBranchTypes(unittest.TestCase):

    def setUp(self):
        inputFile = 'sample_03.root'
        treeName = 'tree'
        inputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), inputFile)

        self.inputFile = ROOT.TFile.Open(inputPath)
        self.tree = self.inputFile.Get(treeName)
        self.events = Events(self.tree)

    def tearDown(self):
        pass

    def test_event(self):

        event = self.events[0]
        self.assertEqual(-125, event.bChar[0])
        self.assertEqual(253, event.bUChar[0])
        self.assertEqual(-10, event.bShort[0])
        self.assertEqual(65530, event.bUShort[0])
        self.assertEqual(-2147483626, event.bInt[0])
        self.assertEqual(4294967290, event.bUInt[0])
        self.assertAlmostEqual(-0.123, event.bFloat[0])
        self.assertAlmostEqual(-2.345, event.bDouble[0])
        self.assertEqual(-4611686018427387900, event.bLong64[0])
        self.assertEqual(9223372036854775802, event.bULong64[0])
        self.assertEqual(1, event.bBool[0])

        event = self.events[1]
        self.assertEqual(127, event.bChar[0])
        self.assertEqual(4, event.bUChar[0])
        self.assertEqual(32765, event.bShort[0])
        self.assertEqual(8, event.bUShort[0])
        self.assertEqual(2147483640, event.bInt[0])
        self.assertEqual(12, event.bUInt[0])
        self.assertAlmostEqual(0.244, event.bFloat[0])
        self.assertAlmostEqual(3.122, event.bDouble[0])
        self.assertEqual(9223372036854775733, event.bLong64[0])
        self.assertEqual(123, event.bULong64[0])
        self.assertEqual(0, event.bBool[0])


##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
@unittest.skipUnless(sys.version_info[0] == 2, "skip for Python 3")
class TestBEventsWithFileVector(unittest.TestCase):

    def test_vector(self):
        inputFile = 'sample_02.root'
        treeName = 'tree'
        inputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), inputFile)

        inputFile = ROOT.TFile.Open(inputPath)
        tree = inputFile.Get(treeName)
        events = Events(tree)

        trigger_path = events.trigger_path
        trigger_decision = events.trigger_decision

        self.assertGreater(tree.GetEntry(0), 0)
        self.assertEqual(449, len(trigger_path))
        self.assertEqual('AlCa_EcalEtaEBonly', trigger_path[0])
        self.assertEqual('DST_Physics', trigger_path[12])
        self.assertEqual('HLT_SingleForJet25', trigger_path[438])
        self.assertEqual(449, len(trigger_decision))
        self.assertEqual(0, trigger_decision[0])
        self.assertEqual(0, trigger_decision[13])
        self.assertEqual(0, trigger_decision[438])

        self.assertGreater(tree.GetEntry(1), 0)
        self.assertEqual(438, len(trigger_path))
        self.assertEqual('AlCa_EcalEtaEBonly', trigger_path[0])
        self.assertEqual('DST_Ele8_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_HT250', trigger_path[12])
        self.assertRaises(IndexError, trigger_path.__getitem__, 438)
        self.assertEqual(438, len(trigger_decision))
        self.assertEqual(0, trigger_decision[0])
        self.assertEqual(1, trigger_decision[13])
        self.assertRaises(IndexError, trigger_decision.__getitem__, 438)

        # This sample file has only two entries. When the 3rd entry is
        # tried to be accessed, GetEntry(2) returns 0, but the vectors
        # won't be cleared. These have the previous contents.
        self.assertEqual(tree.GetEntry(2), 0)
        self.assertEqual(438, len(trigger_path))
        self.assertEqual(438, len(trigger_decision))

##__________________________________________________________________||
