from AlphaTwirl import TblXsec
import pandas
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
    def __init__(self, name, xsec):
        self.name = name
        self._cfg = dict(xSection = xsec)

    def config(self): return self._cfg

##____________________________________________________________________________||
class TestTblXsec(unittest.TestCase):

    def test_read(self):
        tblxsec = TblXsec("t.txt")

        out = cStringIO.StringIO()
        tblxsec._open = MockOpen(out)
        tblxsec._close = mockClose

        tblxsec.begin()

        component = MockComponent("QCD_HT_100To250", 28730000)
        tblxsec.read(component)

        component = MockComponent("TTJets", 809.1)
        tblxsec.read(component)

        component = MockComponent("TBarToLeptons_sch", 1.34784)
        tblxsec.read(component)

        component = MockComponent("TBarToLeptons_tch", 26.23428)
        tblxsec.read(component)

        tblxsec.end()

        expected = '\n'.join([
            '         component            xsec',
            '   QCD_HT_100To250  28730000.00000',
            '            TTJets       809.10000',
            ' TBarToLeptons_sch         1.34784',
            ' TBarToLeptons_tch        26.23428'])
        self.assertEqual(expected, out.getvalue())

##____________________________________________________________________________||
