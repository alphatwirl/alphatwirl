import unittest
import os

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    from AlphaTwirl.Events import BEvents as Events
    from AlphaTwirl.Events import Branch
    hasROOT = True
except ImportError:
    pass

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
@unittest.skip("skip TestBEventsWithFile")
class TestBEventsWithFile(unittest.TestCase):

    def test_branch(self):
        inputFile = 'sample_01.root'
        treeName = 'tree'
        inputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), inputFile)

        inputFile = ROOT.TFile.Open(inputPath)
        tree = inputFile.Get(treeName)
        events = Events(tree)

        jet_pt = events.jet_pt
        met_pt = events.met_pt
        self.assertIsInstance(jet_pt, Branch)
        self.assertIsInstance(met_pt, Branch)

        self.assertEqual(0, len(jet_pt))
        self.assertEqual(1, len(met_pt))
        self.assertEqual(0.0, met_pt[0])

        tree.GetEntry(0)
        self.assertEqual(2, len(jet_pt))
        self.assertEqual(1, len(met_pt))
        self.assertEqual(124.55626678466797, jet_pt[0])
        self.assertEqual(86.90544128417969, jet_pt[1])
        self.assertAlmostEqual(43.783382415771484, met_pt[0])

        tree.GetEntry(1)
        self.assertEqual(3, len(jet_pt))
        self.assertEqual(1, len(met_pt))
        self.assertEqual(112.48554992675781, jet_pt[0])
        self.assertEqual(52.32780075073242, jet_pt[1])
        self.assertEqual(48.861289978027344, jet_pt[2])
        self.assertAlmostEqual(20.483951568603516, met_pt[0])

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
