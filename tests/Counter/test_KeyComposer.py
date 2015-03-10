import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockBinningEcho(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##____________________________________________________________________________||
class MockBinningNone(object):
    def __call__(self, val):
        return None

    def next(self, val):
        return val + 1

##____________________________________________________________________________||
class TestGenericKeyComposer(unittest.TestCase):

    def test_call_1var(self):
        keyComposer = Counter.GenericKeyComposer(('var1', ), (MockBinningEcho(), ))

        event = MockEvent()
        event.var1 = 12
        self.assertEqual((12, ), keyComposer(event))

    def test_call_2vars(self):
        keyComposer = Counter.GenericKeyComposer(('var1', 'var2'), (MockBinningEcho(), MockBinningEcho()))

        event = MockEvent()
        event.var1 = 15
        event.var2 = 22
        self.assertEqual((15, 22), keyComposer(event))

    def test_None_key_1var(self):
        keyComposer = Counter.GenericKeyComposer(('var1', ), (MockBinningNone(), ))

        event = MockEvent()
        event.var1 = 12
        self.assertIsNone(keyComposer(event))

    def test_None_key_2vars_var1(self):
        keyComposer = Counter.GenericKeyComposer(('var1', 'var2'), (MockBinningNone(), MockBinningEcho()))

        event = MockEvent()
        event.var1 = 15
        event.var2 = 22
        self.assertIsNone(keyComposer(event))

    def test_None_key_2vars_var2(self):
        keyComposer = Counter.GenericKeyComposer(('var1', 'var2'), (MockBinningEcho(), MockBinningNone()))

        event = MockEvent()
        event.var1 = 15
        event.var2 = 22
        self.assertIsNone(keyComposer(event))

    def test_binnings(self):
        binning1 = MockBinningEcho()
        keyComposer = Counter.GenericKeyComposer(('var1', ), (binning1, ))
        self.assertEqual((binning1, ), keyComposer.binnings())

        binning1 = MockBinningEcho()
        binning2 = MockBinningEcho()
        keyComposer = Counter.GenericKeyComposer(('var1', 'var2'), (binning1, binning2))
        self.assertEqual((binning1, binning2), keyComposer.binnings())

##____________________________________________________________________________||
