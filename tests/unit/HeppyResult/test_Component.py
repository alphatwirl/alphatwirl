import os
from alphatwirl.heppyresult import Component
import unittest
import pickle

##__________________________________________________________________||
def mock_listdir(path):
    heppyDir = 'dir/201522_SingleMu'
    filesInHeppyDir = ['failed', 'QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets', 'Chunks', 'versionInfo.txt']
    if path == heppyDir:
        return filesInHeppyDir

    components = ['QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets']
    filesInComponent = ['PileUpAnalyzer', 'config.pck', 'config.txt', 'skimAnalyzerCount','treeProducerSusyAlphaT']
    componentDirs = [os.path.join(heppyDir, c) for c in components]
    if path in componentDirs:
        return filesInComponent

    return [ ]

##__________________________________________________________________||
def mock_isdir(path):
    heppyDir = 'dir/201522_SingleMu'
    dirsInHeppy = ['failed', 'QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets', 'Chunks']
    dirsInHeppy = [os.path.join(heppyDir, d) for d in dirsInHeppy]
    if path in dirsInHeppy: return True

    components = ['QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets']
    componentDirs = [os.path.join(heppyDir, c) for c in components]
    dirsInComponent = ['PileUpAnalyzer', 'skimAnalyzerCount','treeProducerSusyAlphaT']
    dirsInComponent = [os.path.join(c, d) for c in componentDirs for d in dirsInComponent]
    if path in dirsInComponent: return True
    return False

##__________________________________________________________________||
def mock_readComponentConfig(path):
    return { "isMC" : "True", 'xSection': '670500' }

##__________________________________________________________________||
class TestComponent(unittest.TestCase):

    def setUp(self):
        self.listdir_org = os.listdir
        os.listdir = mock_listdir

        self.isdir_org = os.path.isdir
        os.path.isdir = mock_isdir

        path = 'dir/201522_SingleMu/QCD_HT_100To250'
        self.component = Component(path)
        self.component._readConfig = mock_readComponentConfig

    def tearDown(self):
        os.listdir = self.listdir_org
        os.path.isdir = self.isdir_org

    def test_init(self):
        self.assertEqual('dir/201522_SingleMu/QCD_HT_100To250', self.component.path)
        self.assertEqual('QCD_HT_100To250', self.component.name)

    def test_analyzerNames(self):
        expected = ['PileUpAnalyzer', 'skimAnalyzerCount','treeProducerSusyAlphaT']
        self.assertEqual(expected, self.component.analyzerNames)

    def test_analyzers_theSameObject(self):
        ana1 = self.component.skimAnalyzerCount
        ana2 = self.component.skimAnalyzerCount
        self.assertIs(ana1, ana2)

    def test_AttributeError(self):
        self.assertRaises(AttributeError, self.component.__getattr__, 'WrongName')

    def test_analyzers(self):
        expected = [self.component.PileUpAnalyzer, self.component.skimAnalyzerCount, self.component.treeProducerSusyAlphaT]
        self.assertEqual(expected, self.component.analyzers())

    def test_config(self):
        expected = { "isMC" : "True", 'xSection': '670500' }
        self.assertEqual(expected, self.component.config())

    def test_config_theSameObject(self):
        cfg1 = self.component.config()
        cfg2 = self.component.config()
        self.assertIs(cfg1, cfg2)

    def test_pickle(self):
        dumps = pickle.dumps(self.component)
        obj = pickle.loads(dumps)

##__________________________________________________________________||
