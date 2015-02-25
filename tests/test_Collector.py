#!/usr/bin/env python
from AlphaTwirl import Collector
import unittest

##____________________________________________________________________________||
class MockReader(object):
    pass

##____________________________________________________________________________||
class MockMethod(object):
    def __init__(self):
        self.readers = None
    def collect(self, readers):
        self.readers = readers

##____________________________________________________________________________||
class TestCollector(unittest.TestCase):

    def test_collect(self):
        method = MockMethod()
        collector = Collector(method)

        reader1 = MockReader()
        collector.addReader('data1', reader1)

        reader2 = MockReader()
        collector.addReader('data2', reader2)

        self.assertIsNone(method.readers)
        collector.collect()
        self.assertEqual([('data1', reader1), ('data2', reader2)], method.readers)

##____________________________________________________________________________||
