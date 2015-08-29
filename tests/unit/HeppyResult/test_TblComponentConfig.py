from AlphaTwirl.HeppyResult import TblComponentConfig
import unittest
import cStringIO

##__________________________________________________________________||
class MockOpen(object):
    def __init__(self, out): self._out = out
    def __call__(self, path): return self._out

##__________________________________________________________________||
def mockClose(file): pass

##__________________________________________________________________||
class MockComponent(object):
    def __init__(self, name, xsec):
        self.name = name
        self._cfg = dict(xSection = xsec)

    def config(self): return self._cfg

##__________________________________________________________________||
class TestTblComponentConfig(unittest.TestCase):

    def test_read(self):
        tblxsec = TblComponentConfig(
            outPath = "t.txt",
            columnNames = ('xsec', ),
            keys = ('xSection', )
        )

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
            '         component     xsec',
            '   QCD_HT_100To250 28730000',
            '            TTJets    809.1',
            ' TBarToLeptons_sch  1.34784',
            ' TBarToLeptons_tch 26.23428']) + '\n'

        self.assertEqual(expected, out.getvalue())

    def test_read_empty(self):
        tblxsec = TblComponentConfig(
            outPath = "t.txt",
            columnNames = ('xsec', ),
            keys = ('xSection', )
        )

        out = cStringIO.StringIO()
        tblxsec._open = MockOpen(out)
        tblxsec._close = mockClose

        tblxsec.begin()
        tblxsec.end()

        expected = ' component xsec\n'
        self.assertEqual(expected, out.getvalue())

##__________________________________________________________________||
