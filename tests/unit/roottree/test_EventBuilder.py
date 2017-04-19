import unittest
import sys

from alphatwirl.roottree import EventBuilderConfig

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.roottree.EventBuilder import EventBuilder

##__________________________________________________________________||
class MockTObject(object):
    def __init__(self, name):
        self.name = name

    def GetEntries(self):
        return 5500

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
        self.moduleEventBuilder = sys.modules['alphatwirl.roottree.EventBuilder']
        self.orgROOT = self.moduleEventBuilder.ROOT
        self.moduleEventBuilder.ROOT = MockROOT()

        self.orgEvents = self.moduleEventBuilder.Events
        self.moduleEventBuilder.Events = MockEvents

    def tearDown(self):
        self.moduleEventBuilder.ROOT = self.orgROOT
        self.moduleEventBuilder.Events = self.orgEvents

    def test_build(self):

        config = EventBuilderConfig(
            inputPath = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root',
            treeName = 'tree',
            maxEvents = 123,
            start = 11,
            name = 'TTJets'
        )

        obj = EventBuilder(config)

        events = obj()

        self.assertEqual('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root', self.moduleEventBuilder.ROOT.TFile.path)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.name)
        self.assertEqual(11, events.start)
        self.assertEqual(123, events.maxEvents)

##__________________________________________________________________||
