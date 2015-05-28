from AlphaTwirl.Events import BEvents as Events
from AlphaTwirl.Events import Branch
import unittest
import os

##____________________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

##____________________________________________________________________________||
inputFile = 'sample_01.root'
treeName = 'tree'

inputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), inputFile)

##____________________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
@unittest.skip("skip TestBEventsWithFile")
class TestBEventsWithFile(unittest.TestCase):

    def test_branch(self):
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

##____________________________________________________________________________||
