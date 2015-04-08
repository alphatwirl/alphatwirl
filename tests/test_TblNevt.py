from AlphaTwirl import TblNevt
import unittest
import cStringIO
import collections

##____________________________________________________________________________||
class MockOpen(object):
    def __init__(self, out): self._out = out
    def __call__(self, path): return self._out

##____________________________________________________________________________||
def mockClose(file): pass

##____________________________________________________________________________||
class MockAnalyzer(object):
    def __init__(self, path): self.path = path

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self, name): self.name = name

##____________________________________________________________________________||
class MockReadCounter(object):
    def __call__(self, path): return self.counter

##____________________________________________________________________________||
class TestTblNevt(unittest.TestCase):

    def test_read(self):
        tblnevt = TblNevt("t.txt")

        out = cStringIO.StringIO()
        tblnevt._open = MockOpen(out)
        tblnevt._close = mockClose

        readCounter = MockReadCounter()
        tblnevt._readCounter = readCounter

        tblnevt.begin()

        component = MockComponent("QCD_HT_100To250")
        component.skimAnalyzerCount = MockAnalyzer('path/to/analyzer')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 4123612, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 4123612.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)

        component = MockComponent("TTJets")
        component.skimAnalyzerCount = MockAnalyzer('path/to/analyzer')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 25446993, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 25446993.0, 'eff2': 1.0, 'eff1': 1.0})])
        tblnevt.read(component)

        component = MockComponent("TBarToLeptons_sch")
        component.skimAnalyzerCount = MockAnalyzer('path/to/analyzer')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 250000, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 320855.887262, 'eff2': 1.2834, 'eff1': 1.28})])
        tblnevt.read(component)

        component = MockComponent("TBarToLeptons_tch")

        component.skimAnalyzerCount = MockAnalyzer('path/to/analyzer')
        readCounter.counter = collections.OrderedDict([('All Events', {'count': 1999800, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 50734279.1235, 'eff2': 25.3697, 'eff1': 25.37})])
        tblnevt.read(component)

        tblnevt.end()

        expected = '\n'.join([
            '         component      nevt    nevt_sumw',
            '   QCD_HT_100To250   4123612  4123612.000',
            '            TTJets  25446993 25446993.000',
            ' TBarToLeptons_sch    250000   320855.887',
            ' TBarToLeptons_tch   1999800 50734279.123']) + '\n'

        self.assertEqual(expected, out.getvalue())


    def test_read_empty(self):
        tblnevt = TblNevt("t.txt")

        out = cStringIO.StringIO()
        tblnevt._open = MockOpen(out)
        tblnevt._close = mockClose

        tblnevt.begin()
        tblnevt.end()

        expected = 'component nevt nevt_sumw\n'
        self.assertEqual(expected, out.getvalue())


##____________________________________________________________________________||
