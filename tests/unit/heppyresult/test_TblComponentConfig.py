from alphatwirl.heppyresult import TblComponentConfig
import unittest
import io

##__________________________________________________________________||
class MockOpen(object):
    def __init__(self, out):
        self._out = out
        self._called = False
    def __call__(self, path):
        self._called = True
        return self._out

##__________________________________________________________________||
def mockClose(file): pass

##__________________________________________________________________||
class MockComponent(object):
    def __init__(self, name, cfg):
        self.name = name
        self._cfg = cfg

    def config(self): return self._cfg

##__________________________________________________________________||
class TestTblComponentConfig(unittest.TestCase):

    def test_read_one_column(self):
        tbl_cfg = TblComponentConfig(
            outPath = "t.txt",
            columnNames = ('xsec', ),
            keys = ('xSection', )
        )

        out = io.BytesIO()
        tbl_cfg._open = MockOpen(out)
        tbl_cfg._close = mockClose

        tbl_cfg.begin()

        component = MockComponent("QCD_HT_100To250", dict(xSection = 28730000))
        tbl_cfg.read(component)

        component = MockComponent("TTJets", dict(xSection = 809.1))
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_sch", dict(xSection = 1.34784))
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_tch", dict(xSection = 26.23428))
        tbl_cfg.read(component)

        tbl_cfg.end()

        expected = '\n'.join([
            '         component     xsec',
            '   QCD_HT_100To250 28730000',
            '            TTJets    809.1',
            ' TBarToLeptons_sch  1.34784',
            ' TBarToLeptons_tch 26.23428']) + '\n'
        expected = expected.encode()

        self.assertEqual(expected, out.getvalue())

    def test_read_two_column(self):
        tbl_cfg = TblComponentConfig(
            outPath = "t.txt",
            columnNames = ('col1', 'col2'),
            keys = ('Column1', 'Column2')
        )

        out = io.BytesIO()
        tbl_cfg._open = MockOpen(out)
        tbl_cfg._close = mockClose

        tbl_cfg.begin()

        component = MockComponent("QCD_HT_100To250", dict(Column1 = 10.0, Column2 = 120.0))
        tbl_cfg.read(component)

        component = MockComponent("TTJets", dict(Column1 = 20.0, Column2 = 130.0))
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_sch", dict(Column1 = 30.0, Column2 = 140.0))
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_tch", dict(Column1 = 40.0, Column2 = 150.0))
        tbl_cfg.read(component)

        tbl_cfg.end()

        expected = '\n'.join([
            '         component col1 col2',
            '   QCD_HT_100To250   10  120',
            '            TTJets   20  130',
            ' TBarToLeptons_sch   30  140',
            ' TBarToLeptons_tch   40  150']) + '\n'
        expected = expected.encode()

        self.assertEqual(expected, out.getvalue())

    def test_read_no_component(self):
        tbl_cfg = TblComponentConfig(
            outPath = "t.txt",
            columnNames = ('xsec', ),
            keys = ('xSection', )
        )

        out = io.BytesIO()
        mockOpen = MockOpen(out)
        tbl_cfg._open = mockOpen
        tbl_cfg._close = mockClose

        tbl_cfg.begin()
        tbl_cfg.end()

        self.assertFalse(mockOpen._called)

    def test_read_no_key_in_some_components(self):
        tbl_cfg = TblComponentConfig(
            outPath = "t.txt",
            columnNames = ('xsec', ),
            keys = ('xSection', )
        )
 
        out = io.BytesIO()
        tbl_cfg._open = MockOpen(out)
        tbl_cfg._close = mockClose

        tbl_cfg.begin()

        component = MockComponent("QCD_HT_100To250", dict(xSection = 28730000))
        tbl_cfg.read(component)

        component = MockComponent("TTJets", dict())
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_sch", dict(xSection = 1.34784))
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_tch", dict())
        tbl_cfg.read(component)

        tbl_cfg.end()

        expected = '\n'.join([
            '         component     xsec',
            '   QCD_HT_100To250 28730000',
            ' TBarToLeptons_sch  1.34784']) + '\n'
        expected = expected.encode()

        self.assertEqual(expected, out.getvalue())

    def test_read_no_key_in_any_components(self):
        tbl_cfg = TblComponentConfig(
            outPath = "t.txt",
            columnNames = ('xsec', ),
            keys = ('xSection', )
        )

        out = io.BytesIO()
        mockOpen = MockOpen(out)
        tbl_cfg._open = mockOpen
        tbl_cfg._close = mockClose

        tbl_cfg.begin()

        component = MockComponent("QCD_HT_100To250", dict())
        tbl_cfg.read(component)

        component = MockComponent("TTJets", dict())
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_sch", dict())
        tbl_cfg.read(component)

        component = MockComponent("TBarToLeptons_tch", dict())
        tbl_cfg.read(component)

        tbl_cfg.end()

        self.assertFalse(mockOpen._called)

##__________________________________________________________________||
