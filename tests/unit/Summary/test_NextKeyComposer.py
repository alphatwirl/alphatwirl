import AlphaTwirl.Summary as Summary
import unittest

##__________________________________________________________________||
class MockBinningPlusOneNext(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##__________________________________________________________________||
class MockBinningNoneNext(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return None

##__________________________________________________________________||
class MockBinningSameNext(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val

##__________________________________________________________________||
class TestNextKeyComposer(unittest.TestCase):

    def test_call(self):
        binnings = (MockBinningPlusOneNext(), MockBinningPlusOneNext(), MockBinningPlusOneNext())
        keyComposer = Summary.NextKeyComposer(binnings)
        self.assertEqual(((12, 8, 20), (11, 9, 20), (11, 8, 21)), keyComposer((11, 8, 20)))

    def test_call_one_none(self):
        binnings = (MockBinningPlusOneNext(), MockBinningNoneNext(), MockBinningPlusOneNext())
        keyComposer = Summary.NextKeyComposer(binnings)
        self.assertEqual(((12, 8, 20), (11, 8, 21)), keyComposer((11, 8, 20)))

    def test_call_all_none(self):
        binnings = (MockBinningNoneNext(), MockBinningNoneNext(), MockBinningNoneNext())
        keyComposer = Summary.NextKeyComposer(binnings)
        self.assertEqual(( ), keyComposer((11, 8, 20)))

    def test_call_no_binning(self):
        binnings = ( )
        keyComposer = Summary.NextKeyComposer(binnings)
        self.assertEqual(( ), keyComposer(( )))

    def test_call_one_same(self):
        binnings = (MockBinningPlusOneNext(), MockBinningSameNext(), MockBinningPlusOneNext())
        keyComposer = Summary.NextKeyComposer(binnings)
        self.assertEqual(((12, 8, 20), (11, 8, 21)), keyComposer((11, 8, 20)))

##__________________________________________________________________||
