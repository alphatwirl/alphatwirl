import unittest
import sys

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    from AlphaTwirl.HeppyResult.EventBuilder import EventBuilder
    hasROOT = True
except ImportError:
    pass

##__________________________________________________________________||
class MockAnalyzer(object):
    def __init__(self):
        self.path = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT'

##__________________________________________________________________||
class MockComponent(object):
    def __init__(self):
        self.treeProducerSusyAlphaT = MockAnalyzer()

##__________________________________________________________________||
class MockTObject(object):
    def __init__(self, name):
        self.name = name
        self.brancheStatus = set()

    def SetBranchStatus(self, bname, status):
        self.brancheStatus.add((bname, status))

##__________________________________________________________________||
class MockTFile(object):
    def Open(self, path):
        self.path = path
        return self
    def Get(self, name):
        return MockTObject(name)

##__________________________________________________________________||
class MockROOT(object):
    def __init__(self): self.TFile = MockTFile()

##__________________________________________________________________||
class MockEvents(object):
    def __init__(self, tree, maxEvents, start = 0):
        self.tree = tree
        self.maxEvents = maxEvents
        self.start = start

##__________________________________________________________________||
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
            analyzerName = 'treeProducerSusyAlphaT', fileName = 'tree.root', treeName = 'tree',
            maxEvents = 1000
            )

        component = MockComponent()
        events = eventBuilder.build(component, start = 10, nEvents = 100)

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(10, events.start)
        self.assertEqual(100, events.maxEvents)
        self.assertEqual(set(), events.tree.brancheStatus)
        self.assertIs(component, events.component)

    def test_build_default_maxEvents_start_nEvents(self):
        eventBuilder = EventBuilder(
            analyzerName = 'treeProducerSusyAlphaT', fileName = 'tree.root', treeName = 'tree'
            # don't give maxEvents
            )

        component = MockComponent()
        events = eventBuilder.build(component) # don't give start or nEvents

        self.assertEqual(0, events.start)
        self.assertEqual(-1, events.maxEvents)

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(set(), events.tree.brancheStatus)
        self.assertIs(component, events.component)

    def test_build_default_maxEvents(self):
        eventBuilder = EventBuilder(
            analyzerName = 'treeProducerSusyAlphaT', fileName = 'tree.root', treeName = 'tree'
            # don't give maxEvents
            )

        component = MockComponent()
        events = eventBuilder.build(component, start = 10, nEvents = 100) # give start or nEvents

        self.assertEqual(10, events.start)
        self.assertEqual(100, events.maxEvents)

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(set(), events.tree.brancheStatus)
        self.assertIs(component, events.component)


    def test_build_default_start_nEvents(self):
        eventBuilder = EventBuilder(
            analyzerName = 'treeProducerSusyAlphaT', fileName = 'tree.root', treeName = 'tree'
            # don't give maxEvents
            )

        component = MockComponent()
        events = eventBuilder.build(component, start = 10, nEvents = 100) # give start or nEvents

        self.assertEqual(10, events.start)
        self.assertEqual(100, events.maxEvents)

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(set(), events.tree.brancheStatus)
        self.assertIs(component, events.component)

    def test_build_maxEvents_smaller_than_nEvents(self):
        eventBuilder = EventBuilder(
            analyzerName = 'treeProducerSusyAlphaT', fileName = 'tree.root', treeName = 'tree',
            maxEvents = 30
            )

        component = MockComponent()
        events = eventBuilder.build(component, start = 10, nEvents = 100)

        self.assertEqual(10, events.start)
        self.assertEqual(30, events.maxEvents)

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(set(), events.tree.brancheStatus)
        self.assertIs(component, events.component)

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

##__________________________________________________________________||
