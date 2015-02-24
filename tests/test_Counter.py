#!/usr/bin/env python
import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockBinning(object):
    def __call__(self, val):
        return val

##____________________________________________________________________________||
class MockCounts(object):
    def __init__(self):
        self._counts = [ ]

    def count(self, key, weight):
        self._counts.append((key, weight))

    def results(self):
        return self._counts

##____________________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class MockKeyComposer(object):
    def __call__(self, event):
        return (11, )

##____________________________________________________________________________||
class TestCounter(unittest.TestCase):

    def test_results(self):
        counter = Counter.Counter(('var', ), MockKeyComposer(), MockCounts(), MockWeightCalculator())
        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counter.results())

##____________________________________________________________________________||
class KeyComposer_SingleVariable(unittest.TestCase):

    def test_call(self):
        keyComposer = Counter.KeyComposer_SingleVariable('var1', MockBinning())

        event = MockEvent()
        event.var1 = 12
        self.assertEqual((12, ), keyComposer(event))

##____________________________________________________________________________||
class KeyComposer_TwoVariables(unittest.TestCase):

    def test_call(self):
        keyComposer = Counter.KeyComposer_TwoVariables('var1', MockBinning(), 'var2', MockBinning())

        event = MockEvent()
        event.var1 = 15
        event.var2 = 22
        self.assertEqual((15, 22), keyComposer(event))

##____________________________________________________________________________||
