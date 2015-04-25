import unittest
import sys

##____________________________________________________________________________||
hasROOT = False
try:
    import ROOT
    from AlphaTwirl.HeppyResult.EventBuilder import EventBuilder
    hasROOT = True
except ImportError:
    pass

##____________________________________________________________________________||
class MockAnalyzer(object):
    def __init__(self):
        self.path = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT'

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self):
        self.treeProducerSusyAlphaT = MockAnalyzer()

##____________________________________________________________________________||
class MockTObject(object):
    def __init__(self, name):
        self.name = name
        self.brancheStatus = set()

    def SetBranchStatus(self, bname, status):
        self.brancheStatus.add((bname, status))

##____________________________________________________________________________||
class MockTFile(object):
    def Open(self, path):
        self.path = path
        return self
    def Get(self, name):
        return MockTObject(name)

##____________________________________________________________________________||
class MockROOT(object):
    def __init__(self): self.TFile = MockTFile()

##____________________________________________________________________________||
class MockEvents(object):
    def __init__(self, tree, maxEvents):
        self.tree = tree
        self.maxEvents = maxEvents

##____________________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestEventBuilder(unittest.TestCase):

    def setUp(self):
        self.moduleEventBuilder = sys.modules['AlphaTwirl.HeppyResult.EventBuilder']
        self.orgROOT = self.moduleEventBuilder.ROOT
        self.moduleEventBuilder.ROOT = MockROOT()

        self.orgEvents = self.moduleEventBuilder.Events
        self.moduleEventBuilder.Events = MockEvents

    def tearDown(self):
        self.moduleEventBuilder.ROOT = self.orgROOT
        self.moduleEventBuilder.Events = self.orgEvents

    def test_build(self):
        eventBuilder = EventBuilder(
            analyzerName = 'treeProducerSusyAlphaT',
            fileName = 'tree.root',
            treeName = 'tree',
            maxEvents = 100)

        component = MockComponent()
        events = eventBuilder.build(component)

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(100, events.maxEvents)
        self.assertEqual(set(), events.tree.brancheStatus)

    def test_build_brancheNames(self):
        eventBuilder = EventBuilder(
            analyzerName = 'treeProducerSusyAlphaT',
            fileName = 'tree.root',
            treeName = 'tree',
            maxEvents = 100,
            brancheNames = set(['met_pt', 'jet_pt', 'nJet40', 'nBJet40'])
        )

        component = MockComponent()
        events = eventBuilder.build(component)

        expected = set([('*', 0), ('nBJet40', 1), ('met_pt', 1), ('nJet40', 1), ('jet_pt', 1)])
        self.assertEqual(expected, events.tree.brancheStatus)

##____________________________________________________________________________||
