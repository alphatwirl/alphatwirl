import unittest
import sys

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    from AlphaTwirl.HeppyResult.BEventBuilder import BEventBuilder
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
    def __init__(self, tree, maxEvents):
        self.tree = tree
        self.maxEvents = maxEvents

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestBEventBuilder(unittest.TestCase):

    def setUp(self):
        self.moduleBEventBuilder = sys.modules['AlphaTwirl.HeppyResult.BEventBuilder']
        self.orgROOT = self.moduleBEventBuilder.ROOT
        self.moduleBEventBuilder.ROOT = MockROOT()

        self.orgEvents = self.moduleBEventBuilder.BEvents
        self.moduleBEventBuilder.BEvents = MockEvents

    def tearDown(self):
        self.moduleBEventBuilder.ROOT = self.orgROOT
        self.moduleBEventBuilder.BEvents = self.orgEvents

    def test_build(self):
        eventBuilder = BEventBuilder(
            analyzerName = 'treeProducerSusyAlphaT',
            fileName = 'tree.root',
            treeName = 'tree',
            maxEvents = 100)

        component = MockComponent()
        events = eventBuilder.build(component)

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleBEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(100, events.maxEvents)
        self.assertIs(component, events.component)

##__________________________________________________________________||
