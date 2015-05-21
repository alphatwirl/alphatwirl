import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockBinningEcho(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##____________________________________________________________________________||
class TestNextKeyComposer(unittest.TestCase):

    def test_next(self):
        binnings = (MockBinningEcho(), MockBinningEcho(), MockBinningEcho())
        keyComposer = Counter.NextKeyComposer(binnings)
        self.assertEqual(((12, 8, 20), (11, 9, 20), (11, 8, 21)), keyComposer((11, 8, 20)))

##____________________________________________________________________________||
