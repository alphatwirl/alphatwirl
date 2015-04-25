from AlphaTwirl.HeppyResult.EventBuilder import EventBuilder
import unittest
import sys

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
    def __init__(self, name): self.name = name

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

##____________________________________________________________________________||
