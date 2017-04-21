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
class MockTChain(object):
    def __init__(self, name):
        self.treeName = name
        self.paths = [ ]

    def Add(self, name):
        self.paths.append(name)

##__________________________________________________________________||
class MockROOT(object):
    def __init__(self):
        self.TChain = MockTChain

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
        self.module = sys.modules['alphatwirl.roottree.EventBuilder']
        self.orgROOT = self.module.ROOT
        self.module.ROOT = MockROOT()

        self.orgEvents = self.module.Events
        self.module.Events = MockEvents

    def tearDown(self):
        self.module.ROOT = self.orgROOT
        self.module.BEvents = self.orgEvents

    def test_build(self):

        config = EventBuilderConfig(
            inputPaths = ['/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root'],
            treeName = 'tree',
            maxEvents = 123,
            start = 11,
            name = 'TTJets'
        )

        obj = EventBuilder(config)

        events = obj()

        self.assertEqual(['/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root'], events.tree.paths)
        self.assertIsInstance(events, MockEvents)
        self.assertEqual('tree', events.tree.treeName)
        self.assertEqual(11, events.start)
        self.assertEqual(123, events.maxEvents)

##__________________________________________________________________||
