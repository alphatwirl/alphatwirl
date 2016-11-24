import sys
import unittest

from AlphaTwirl.HeppyResult import Chunk

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    from AlphaTwirl.HeppyResult import ComponentSplitter
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
        self.name = 'TTJets'

##__________________________________________________________________||
class MockTObject(object):
    def __init__(self, name):
        self.name = name

    def GetEntries(self):
        return 2500

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
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestComponentSplitter(unittest.TestCase):

    def setUp(self):
        self.moduleComponentSplitter = sys.modules['AlphaTwirl.HeppyResult.ComponentSplitter']
        self.orgROOT = self.moduleComponentSplitter.ROOT
        self.moduleComponentSplitter.ROOT = MockROOT()

    def tearDown(self):
        self.moduleComponentSplitter.ROOT = self.orgROOT

    def test_init_raise(self):

        self.assertRaises(ValueError, ComponentSplitter,
                          analyzerName = 'treeProducerSusyAlphaT',
                          fileName = 'tree.root',
                          treeName = 'tree',
                          maxEventsPerRun = 0
        )

    def test_split_one_chunk(self):
        obj = ComponentSplitter(
            analyzerName = 'treeProducerSusyAlphaT',
            fileName = 'tree.root',
            treeName = 'tree'
        )

        component = MockComponent()

        expected = [
            Chunk(
                inputPath = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root',
                treeName = 'tree',
                maxEvents = -1,
                start = 0,
                component = component,
                name = 'TTJets'
            )
        ]

        self.assertEqual(expected, obj.split(component))

    def test_split_multiple_chunks(self):
        obj = ComponentSplitter(
            analyzerName = 'treeProducerSusyAlphaT',
            fileName = 'tree.root',
            treeName = 'tree',
            maxEvents = -1,
            maxEventsPerRun = 1000
        )

        component = MockComponent()

        expected = [
            Chunk(
                inputPath = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root',
                treeName = 'tree',
                maxEvents = 1000,
                start = 0,
                component = component,
                name = 'TTJets'
            ),
            Chunk(
                inputPath = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root',
                treeName = 'tree',
                maxEvents = 1000,
                start = 1000,
                component = component,
                name = 'TTJets'
            ),
            Chunk(
                inputPath = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root',
                treeName = 'tree',
                maxEvents = 500,
                start = 2000,
                component = component,
                name = 'TTJets'
            ),
        ]

        self.assertEqual(expected, obj.split(component))

##__________________________________________________________________||
