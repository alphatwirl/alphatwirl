import os
from alphatwirl.heppyresult import Analyzer
import unittest

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
class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.listdir_org = os.listdir
        self.isdir_org = os.path.isdir
        os.listdir = mock_listdir
        os.path.isdir = mock_isdir

        path = 'dir/201522_SingleMu/QCD_HT_100To250/PileUpAnalyzer'
        self.analyzer = Analyzer(path)

    def tearDown(self):
        os.listdir = self.listdir_org
        os.path.isdir = self.isdir_org

    def test_init(self):
        self.assertEqual('dir/201522_SingleMu/QCD_HT_100To250/PileUpAnalyzer', self.analyzer.path)
        self.assertEqual('PileUpAnalyzer', self.analyzer.name)


##__________________________________________________________________||
