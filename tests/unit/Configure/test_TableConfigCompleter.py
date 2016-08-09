import unittest
import os

from AlphaTwirl.Configure import TableConfigCompleter

##__________________________________________________________________||
class MockDefaultSummary: pass

##__________________________________________________________________||
class MockSummary2: pass

##__________________________________________________________________||
class MockWeight: pass

##__________________________________________________________________||
class MockBinning: pass

##__________________________________________________________________||
class TestTableConfigCompleter(unittest.TestCase):

    def test_copy(self):
        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
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
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(('met_pt', ), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertIsNone(tblcfg_out['keyIndices'])
        self.assertIsNone(tblcfg_out['valAttrNames'])
        self.assertIsNone(tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockDefaultSummary, tblcfg_out['summaryClass'])

        self.assertEqual(('met_pt', ), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(('n', 'nvar'), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_n_component_met_pt.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_n_component_met_pt.txt'), tblcfg_out['outFilePath'])

    def test_default_summary_class_empty_key(self):
        tblcfg_in = dict(
            keyAttrNames = ( ),
            binnings = ( )
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(( ), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertIsNone(tblcfg_out['keyIndices'])
        self.assertIsNone(tblcfg_out['valAttrNames'])
        self.assertIsNone(tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockDefaultSummary, tblcfg_out['summaryClass'])

        self.assertEqual(( ), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(('n', 'nvar'), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_n_component.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_n_component.txt'), tblcfg_out['outFilePath'])

    def test_specify_summary_class_empty_key_empty_val(self):
        tblcfg_in = dict(
            keyAttrNames = ( ),
            binnings = ( ),
            summaryClass = MockSummary2,
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(( ), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertIsNone(tblcfg_out['keyIndices'])
        self.assertIsNone(tblcfg_out['valAttrNames'])
        self.assertIsNone(tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockSummary2, tblcfg_out['summaryClass'])

        self.assertEqual(( ), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(( ), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_MockSummary2.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_MockSummary2.txt'), tblcfg_out['outFilePath'])

    def test_specify_summary_class_2_keys_empty_vals(self):
        tblcfg_in = dict(
            keyAttrNames = ('key1', 'key2'),
            binnings = (MockBinning(), MockBinning()),
            summaryClass = MockSummary2,
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertIsNone(tblcfg_out['keyIndices'])
        self.assertIsNone(tblcfg_out['valAttrNames'])
        self.assertIsNone(tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockSummary2, tblcfg_out['summaryClass'])

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(( ), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_MockSummary2_key1_key2.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_MockSummary2_key1_key2.txt'), tblcfg_out['outFilePath'])

    def test_specify_summary_class_2_keys_2_vals(self):
        tblcfg_in = dict(
            keyAttrNames = ('key1', 'key2'),
            binnings = (MockBinning(), MockBinning()),
            valAttrNames = ('val1', 'val2'),
            summaryClass = MockSummary2,
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertIsNone(tblcfg_out['keyIndices'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valAttrNames'])
        self.assertIsNone(tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockSummary2, tblcfg_out['summaryClass'])

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_MockSummary2_key1_key2_val1_val2.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_MockSummary2_key1_key2_val1_val2.txt'), tblcfg_out['outFilePath'])

    def test_specify_summary_class_2_keys_2_vals_key_indices(self):
        tblcfg_in = dict(
            keyAttrNames = ('key1', 'key2'),
            binnings = (MockBinning(), MockBinning()),
            keyIndices = (None, 1),
            valAttrNames = ('val1', 'val2'),
            summaryClass = MockSummary2,
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertEqual((None, 1), tblcfg_out['keyIndices'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valAttrNames'])
        self.assertIsNone(tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockSummary2, tblcfg_out['summaryClass'])

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_MockSummary2_key1_key2_1_val1_val2.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_MockSummary2_key1_key2_1_val1_val2.txt'), tblcfg_out['outFilePath'])

    def test_specify_summary_class_2_keys_2_vals_val_indices(self):
        tblcfg_in = dict(
            keyAttrNames = ('key1', 'key2'),
            binnings = (MockBinning(), MockBinning()),
            valAttrNames = ('val1', 'val2'),
            summaryClass = MockSummary2,
            valIndices = (2, None),
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertIsNone(tblcfg_out['keyIndices'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valAttrNames'])
        self.assertEqual((2, None), tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockSummary2, tblcfg_out['summaryClass'])

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_MockSummary2_key1_key2_val1_2_val2.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_MockSummary2_key1_key2_val1_2_val2.txt'), tblcfg_out['outFilePath'])

    def test_specify_summary_class_2_keys_2_vals_key_indices_val_indices(self):
        tblcfg_in = dict(
            keyAttrNames = ('key1', 'key2'),
            binnings = (MockBinning(), MockBinning()),
            keyIndices = (None, 1),
            valAttrNames = ('val1', 'val2'),
            summaryClass = MockSummary2,
            valIndices = (2, 3),
        )

        obj = TableConfigCompleter(
            defaultSummaryClass = MockDefaultSummary,
            defaultWeight = MockWeight(),
            defaultOutDir = 'tmp'
        )

        tblcfg_out = obj.complete(tblcfg_in)

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyAttrNames'])
        self.assertEqual(tblcfg_in['binnings'], tblcfg_out['binnings'])
        self.assertEqual((None, 1), tblcfg_out['keyIndices'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valAttrNames'])
        self.assertEqual((2, 3), tblcfg_out['valIndices'])

        self.assertIs(obj.defaultWeight, tblcfg_out['weight'])

        self.assertIs(MockSummary2, tblcfg_out['summaryClass'])

        self.assertEqual(('key1', 'key2'), tblcfg_out['keyOutColumnNames'])
        self.assertEqual(('val1', 'val2'), tblcfg_out['valOutColumnNames'])

        self.assertTrue(tblcfg_out['outFile'])
        self.assertEqual('tbl_MockSummary2_key1_key2_1_val1_2_val2_3.txt', tblcfg_out['outFileName'])
        self.assertEqual(os.path.join('tmp', 'tbl_MockSummary2_key1_key2_1_val1_2_val2_3.txt'), tblcfg_out['outFilePath'])

##__________________________________________________________________||
