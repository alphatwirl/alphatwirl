from alphatwirl.heppyresult import TblCounterLong
import unittest
import io
import collections

##__________________________________________________________________||
class MockOpen(object):
    def __init__(self, out): self._out = out
    def __call__(self, path): return self._out

##__________________________________________________________________||
def mockClose(file): pass

##__________________________________________________________________||
class MockAnalyzer(object):
    def __init__(self, path): self.path = path

##__________________________________________________________________||
class MockComponent(object):
    def __init__(self, name): self.name = name

##__________________________________________________________________||
class MockReadCounter(object):
    def __call__(self, path):
        self.path = path
        return self.counter

##__________________________________________________________________||
class TestTblCounterLong(unittest.TestCase):

    def test_read(self):
        tblnevt = TblCounterLong(
            analyzerName = 'skimAnalyzerCount',
            fileName = 'SkimReport.txt',
            outPath = "t.txt",
            levels = ('All Events', 'Sum Weights'),
            columnNames = ('component', 'type', 'n')
        )

        out = io.BytesIO()
        tblnevt._open = MockOpen(out)
        tblnevt._close = mockClose

        readCounter = MockReadCounter()
        tblnevt._readCounter = readCounter

        tblnevt.begin()

        component = MockComponent("QCD_HT_100To250")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/QCD_HT_100To250/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 4123612, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 4123612.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/QCD_HT_100To250/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TTJets")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TTJets/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 25446993, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 25446993.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TTJets/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TBarToLeptons_sch")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TBarToLeptons_sch/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 250000, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 320855.887262, 'eff2': 1.2834, 'eff1': 1.28})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TBarToLeptons_sch/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TBarToLeptons_tch")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TBarToLeptons_tch/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 1999800, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 50734279.1235, 'eff2': 25.3697, 'eff1': 25.37})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TBarToLeptons_tch/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        tblnevt.end()

        expected = '\n'.join([
            '         component          type             n',
            '   QCD_HT_100To250  "All Events"       4123612',
            '   QCD_HT_100To250 "Sum Weights"       4123612',
            '            TTJets  "All Events"      25446993',
            '            TTJets "Sum Weights"      25446993',
            ' TBarToLeptons_sch  "All Events"        250000',
            ' TBarToLeptons_sch "Sum Weights" 320855.887262',
            ' TBarToLeptons_tch  "All Events"       1999800',
            ' TBarToLeptons_tch "Sum Weights" 50734279.1235']) + '\n'
        expected = expected.encode()

        self.assertEqual(expected, out.getvalue())


    def test_read_default_columnNames(self):
        tblnevt = TblCounterLong(
            analyzerName = 'skimAnalyzerCount',
            fileName = 'SkimReport.txt',
            outPath = "t.txt",
            levels = ('All Events', 'Sum Weights')
        )

        out = io.BytesIO()
        tblnevt._open = MockOpen(out)
        tblnevt._close = mockClose

        readCounter = MockReadCounter()
        tblnevt._readCounter = readCounter

        tblnevt.begin()

        component = MockComponent("QCD_HT_100To250")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/QCD_HT_100To250/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 4123612, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 4123612.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/QCD_HT_100To250/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TTJets")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TTJets/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 25446993, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 25446993.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TTJets/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TBarToLeptons_sch")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TBarToLeptons_sch/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 250000, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 320855.887262, 'eff2': 1.2834, 'eff1': 1.28})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TBarToLeptons_sch/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TBarToLeptons_tch")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TBarToLeptons_tch/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 1999800, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 50734279.1235, 'eff2': 25.3697, 'eff1': 25.37})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TBarToLeptons_tch/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        tblnevt.end()

        expected = '\n'.join([
            '         component         level         count',
            '   QCD_HT_100To250  "All Events"       4123612',
            '   QCD_HT_100To250 "Sum Weights"       4123612',
            '            TTJets  "All Events"      25446993',
            '            TTJets "Sum Weights"      25446993',
            ' TBarToLeptons_sch  "All Events"        250000',
            ' TBarToLeptons_sch "Sum Weights" 320855.887262',
            ' TBarToLeptons_tch  "All Events"       1999800',
            ' TBarToLeptons_tch "Sum Weights" 50734279.1235']) + '\n'
        expected = expected.encode()

        self.assertEqual(expected, out.getvalue())


    def test_read_default_levels(self):
        tblnevt = TblCounterLong(
            analyzerName = 'skimAnalyzerCount',
            fileName = 'SkimReport.txt',
            outPath = "t.txt"
        )

        out = io.BytesIO()
        tblnevt._open = MockOpen(out)
        tblnevt._close = mockClose

        readCounter = MockReadCounter()
        tblnevt._readCounter = readCounter

        tblnevt.begin()

        component = MockComponent("QCD_HT_100To250")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/QCD_HT_100To250/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 4123612, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 4123612.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/QCD_HT_100To250/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TTJets")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TTJets/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 25446993, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 25446993.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TTJets/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TBarToLeptons_sch")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TBarToLeptons_sch/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 250000, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 320855.887262, 'eff2': 1.2834, 'eff1': 1.28})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TBarToLeptons_sch/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        component = MockComponent("TBarToLeptons_tch")
        component.skimAnalyzerCount = MockAnalyzer('201525_SingleMu/TBarToLeptons_tch/skimAnalyzerCount')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 1999800, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 50734279.1235, 'eff2': 25.3697, 'eff1': 25.37})])
        tblnevt.read(component)
        self.assertEqual('201525_SingleMu/TBarToLeptons_tch/skimAnalyzerCount/SkimReport.txt', readCounter.path)

        tblnevt.end()

        expected = '\n'.join([
            '         component         level         count',
            '   QCD_HT_100To250  "All Events"       4123612',
            '   QCD_HT_100To250 "Sum Weights"       4123612',
            '            TTJets  "All Events"      25446993',
            '            TTJets "Sum Weights"      25446993',
            ' TBarToLeptons_sch  "All Events"        250000',
            ' TBarToLeptons_sch "Sum Weights" 320855.887262',
            ' TBarToLeptons_tch  "All Events"       1999800',
            ' TBarToLeptons_tch "Sum Weights" 50734279.1235']) + '\n'
        expected = expected.encode()

        self.assertEqual(expected, out.getvalue())


    def test_read_empty(self):
        tblnevt = TblCounterLong(
            analyzerName = 'skimAnalyzerCount',
            fileName = 'SkimReport.txt',
            outPath = "t.txt",
        )

        out = io.BytesIO()
        tblnevt._open = MockOpen(out)
        tblnevt._close = mockClose

        tblnevt.begin()
        tblnevt.end()

        expected = ' component level count\n'.encode()
        self.assertEqual(expected, out.getvalue())

##__________________________________________________________________||
