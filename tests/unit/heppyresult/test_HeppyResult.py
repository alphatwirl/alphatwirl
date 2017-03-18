import os
from alphatwirl.heppyresult import HeppyResult
import unittest

##__________________________________________________________________||
def mock_listdir(path):
    heppyDir = 'dir/201522_SingleMu'
    filesInHeppyDir = ['failed', 'QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets', 'Chunks', 'versionInfo.txt', 'AnotherDir']
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
    dirsInHeppy = ['failed', 'QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets', 'Chunks', 'AnotherDir']
    dirsInHeppy = [os.path.join(heppyDir, d) for d in dirsInHeppy]
    if path in dirsInHeppy: return True

    components = ['QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets']
    componentDirs = [os.path.join(heppyDir, c) for c in components]
    dirsInComponent = ['PileUpAnalyzer', 'skimAnalyzerCount','treeProducerSusyAlphaT']
    dirsInComponent = [os.path.join(c, d) for c in componentDirs for d in dirsInComponent]
    if path in dirsInComponent: return True
    return False

##__________________________________________________________________||
def mock_readVersionInfo(path):
    return {
        'tag': 'RA1cmg_v2.3',
        'full': 'Tag for production: \nRA1cmg_v2.3\n\nExtra information: \n'
    }

##__________________________________________________________________||
class TestHeppyResult(unittest.TestCase):

    def setUp(self):
        self.listdir_org = os.listdir
        self.isdir_org = os.path.isdir
        os.listdir = mock_listdir
        os.path.isdir = mock_isdir

        path = 'dir/201522_SingleMu'
        self.heppy = HeppyResult(path)
        self.heppy._readVersionInfo = mock_readVersionInfo

    def tearDown(self):
        os.listdir = self.listdir_org
        os.path.isdir = self.isdir_org

    def test_init(self):
        self.assertEqual('dir/201522_SingleMu', self.heppy.path)

    def test_trailing_slash(self):
        heppy = HeppyResult('dir/201522_SingleMu/')
        self.assertEqual('dir/201522_SingleMu', heppy.path)

    def test_componentNames(self):
        expected = ['QCD_HT_100To250', 'QCD_HT_250To500', 'TTJets']
        self.assertEqual(expected, self.heppy.componentNames)

    def test_components_theSameObject(self):
        comp1 = self.heppy.QCD_HT_100To250
        comp2 = self.heppy.QCD_HT_100To250
        self.assertIs(comp1, comp2)

    def test_AttributeError(self):
        self.assertRaises(AttributeError, self.heppy.__getattr__, 'WrongName')

    def test_components(self):
        expected = [self.heppy.QCD_HT_100To250, self.heppy.QCD_HT_250To500, self.heppy.TTJets]
        self.assertEqual(expected, self.heppy.components())

    def test_init_with_componentNames(self):
        path = 'dir/201522_SingleMu'
        componentNames = ['QCD_HT_100To250', 'QCD_HT_250To500']
        heppy = HeppyResult(path = path, componentNames = componentNames)

        expected = componentNames
        self.assertEqual(expected, heppy.componentNames)

    def test_init_with_componentNames_wrongName(self):
        path = 'dir/201522_SingleMu'
        componentNames = ['QCD_HT_100To250', 'QCD_HT_250To500', 'WrongName']
        self.assertRaises(ValueError, HeppyResult, path = path, componentNames = componentNames)

    def test_init_with_componentNames_AnotherDir (self):
        path = 'dir/201522_SingleMu'
        componentNames = ['QCD_HT_100To250', 'QCD_HT_250To500', 'AnotherDir']
        self.assertRaises(ValueError, HeppyResult, path = path, componentNames = componentNames)

    def test_init_with_excludeList(self):
        path = 'dir/201522_SingleMu'
        excludeList = ('failed', 'QCD_HT_100To250')
        heppy = HeppyResult(path = path, excludeList = excludeList)

        expected = ['QCD_HT_250To500', 'TTJets']
        self.assertEqual(expected, heppy.componentNames)

    def test_versionInfo(self):
        expected = {
            'tag': 'RA1cmg_v2.3',
            'full': 'Tag for production: \nRA1cmg_v2.3\n\nExtra information: \n'
        }
        self.assertEqual(expected, self.heppy.versionInfo())

    def test_versionInfo_theSameObject(self):
        info1 = self.heppy.versionInfo()
        info2 = self.heppy.versionInfo()
        self.assertIs(info1, info2)

##__________________________________________________________________||
