#!/usr/bin/env python
import os
from alphatwirl import Heppy
import unittest

##____________________________________________________________________________||
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

##____________________________________________________________________________||
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

##____________________________________________________________________________||
class TestHeppy(unittest.TestCase):

    def setUp(self):
        self.listdir_org = Heppy.os.listdir
        self.isdir_org = Heppy.os.path.isdir
        Heppy.os.listdir = mock_listdir
        Heppy.os.path.isdir = mock_isdir

        path = 'dir/201522_SingleMu'
        self.heppy = Heppy.Heppy(path)

    def tearDown(self):
        Heppy.os.listdir = self.listdir_org
        Heppy.os.path.isdir = self.isdir_org

    def test_init(self):
        self.assertEqual('dir/201522_SingleMu', self.heppy.path)

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


##____________________________________________________________________________||
class TestComponent(unittest.TestCase):

    def setUp(self):
        self.listdir_org = Heppy.os.listdir
        self.isdir_org = Heppy.os.path.isdir
        Heppy.os.listdir = mock_listdir
        Heppy.os.path.isdir = mock_isdir

        path = 'dir/201522_SingleMu/QCD_HT_100To250'
        self.component = Heppy.Component(path)

    def tearDown(self):
        Heppy.os.listdir = self.listdir_org
        Heppy.os.path.isdir = self.isdir_org

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

##____________________________________________________________________________||
class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.listdir_org = Heppy.os.listdir
        self.isdir_org = Heppy.os.path.isdir
        Heppy.os.listdir = mock_listdir
        Heppy.os.path.isdir = mock_isdir

        path = 'dir/201522_SingleMu/QCD_HT_100To250/PileUpAnalyzer'
        self.analyzer = Heppy.Analyzer(path)

    def tearDown(self):
        Heppy.os.listdir = self.listdir_org
        Heppy.os.path.isdir = self.isdir_org

    def test_init(self):
        self.assertEqual('dir/201522_SingleMu/QCD_HT_100To250/PileUpAnalyzer', self.analyzer.path)
        self.assertEqual('PileUpAnalyzer', self.analyzer.name)


##____________________________________________________________________________||
