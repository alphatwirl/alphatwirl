import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockBinning(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##____________________________________________________________________________||
class TestKeyComposer_SingleVariable(unittest.TestCase):

    def test_call(self):
        keyComposer = Counter.KeyComposer_SingleVariable('var1', MockBinning())

        event = MockEvent()
        event.var1 = 12
        self.assertEqual((12, ), keyComposer(event))

    def test_binnings(self):
        binning1 = MockBinning()
        keyComposer = Counter.KeyComposer_SingleVariable('var1', binning1)
        self.assertEqual((binning1, ), keyComposer.binnings())

##____________________________________________________________________________||
class TestKeyComposer_TwoVariables(unittest.TestCase):

    def test_call(self):
        keyComposer = Counter.KeyComposer_TwoVariables('var1', MockBinning(), 'var2', MockBinning())

        event = MockEvent()
        event.var1 = 15
        event.var2 = 22
        self.assertEqual((15, 22), keyComposer(event))

    def test_binnings(self):
        binning1 = MockBinning()
        binning2 = MockBinning()
        keyComposer = Counter.KeyComposer_TwoVariables('var1', binning1, 'var2', binning2)
        self.assertEqual((binning1, binning2), keyComposer.binnings())

##____________________________________________________________________________||
