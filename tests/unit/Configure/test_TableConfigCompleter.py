from AlphaTwirl.Configure import TableConfigCompleter
import unittest

##__________________________________________________________________||
class MockCounts: pass

##__________________________________________________________________||
class MockWeight: pass

##__________________________________________________________________||
class MockBinning: pass

##__________________________________________________________________||
class TestTableConfigCompleter(unittest.TestCase):

    def test_copy(self):
        completer = TableConfigCompleter(
            defaultCountsClass = MockCounts,
            defaultWeight = MockWeight(),
            defaultOutDir = '/tmp'
        )
        tblcfg_in = dict(branchNames = ('met_pt', ), binnings = (MockBinning(), ))
        tblcfg_out = completer.complete(tblcfg_in)
        self.assertIsNot(tblcfg_in, tblcfg_out)

    def test_minimum_input(self):
        completer = TableConfigCompleter(
            defaultCountsClass = MockCounts,
            defaultWeight = MockWeight(),
            defaultOutDir = '/tmp'
        )

        tblcfg_in = dict(branchNames = ('met_pt', ), binnings = (MockBinning(), ))
        tblcfg_out = completer.complete(tblcfg_in)
        self.assertEqual(('met_pt', ), tblcfg_out['outColumnNames'])
        self.assertIsNone(tblcfg_out['indices'])
        self.assertIs(MockCounts, tblcfg_out['countsClass'])
        self.assertTrue(tblcfg_out['outFile'])
        self.assertIs(completer.defaultWeight, tblcfg_out['weight'])
        self.assertEqual('tbl_component_met_pt.txt', tblcfg_out['outFileName'])
        self.assertEqual('/tmp/tbl_component_met_pt.txt', tblcfg_out['outFilePath'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertEqual(('met_pt', ), tblcfg_out['branchNames'])

##__________________________________________________________________||
