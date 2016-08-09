from AlphaTwirl.Configure import TableConfigCompleter
import unittest

##__________________________________________________________________||
class MockCount: pass

##__________________________________________________________________||
class MockCount2: pass

##__________________________________________________________________||
class MockWeight: pass

##__________________________________________________________________||
class MockBinning: pass

##__________________________________________________________________||
class TestTableConfigCompleter(unittest.TestCase):

    def test_copy(self):
        obj = TableConfigCompleter(
            defaultSummaryClass = MockCount,
            defaultWeight = MockWeight(),
            defaultOutDir = '/tmp'
        )
        tblcfg_in = dict(keyAttrNames = ('met_pt', ), binnings = (MockBinning(), ))
        tblcfg_out = obj.complete(tblcfg_in)
        self.assertIsNot(tblcfg_in, tblcfg_out)

    def test_minimum_input(self):
        tblcfg_in = dict(
            keyAttrNames = ('met_pt', ),
            binnings = (MockBinning(), )
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockCount,
            defaultWeight = MockWeight(),
            defaultOutDir = '/tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(('met_pt', ), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertIsNone(tblcfg_out['keyIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockCount, tblcfg_out['summaryClass'])

        self.assertEqual(('met_pt', ), tblcfg_out['keyOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_n_component_met_pt.txt', tblcfg_out['outFileName'])
        self.assertEqual('/tmp/tbl_n_component_met_pt.txt', tblcfg_out['outFilePath'])

##__________________________________________________________________||
