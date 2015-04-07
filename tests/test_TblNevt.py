from AlphaTwirl import TblNevt
import unittest
import cStringIO

##____________________________________________________________________________||
class MockOpen(object):
    def __init__(self, out): self._out = out
    def __call__(self, path): return self._out

##____________________________________________________________________________||
def mockClose(file): pass

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self, name, nevt):
        self.name = name
        self.nevt = nevt

##____________________________________________________________________________||
class MockGetNEventsFor(object):
    def __init__(self): self._nevt = 0
    def __call__(self, component): return component.nevt

##____________________________________________________________________________||
class TestTblNevt(unittest.TestCase):

    def test_read(self):
        tblnevt = TblNevt("t.txt")

        out = cStringIO.StringIO()
        tblnevt._open = MockOpen(out)
        tblnevt._close = mockClose

        getNEventsFor = MockGetNEventsFor()
        tblnevt._getNEventsFor = getNEventsFor

        tblnevt.begin()

        component = MockComponent("QCD_HT_100To250", 4123612)
        tblnevt.read(component)

        component = MockComponent("TTJets", 25446993)
        tblnevt.read(component)

        component = MockComponent("TBarToLeptons_sch", 320855.887262)
        tblnevt.read(component)

        component = MockComponent("TBarToLeptons_tch", 50734279.1235)
        tblnevt.read(component)

        tblnevt.end()

        expected = '\n'.join([
            '         component          nevt',
            '   QCD_HT_100To250   4123612.000',
            '            TTJets  25446993.000',
            ' TBarToLeptons_sch    320855.887',
            ' TBarToLeptons_tch  50734279.123'])
        self.assertEqual(expected, out.getvalue())


##____________________________________________________________________________||
