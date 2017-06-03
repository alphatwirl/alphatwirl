import unittest

import collections

from alphatwirl.loop import Collector

##__________________________________________________________________||
class MockResultsCombinationMethod(object):
    def __init__(self, ret = None):
        self.ret = ret

    def combine(self, dataset_readers_list):
        self.args = dataset_readers_list
        return self.ret

##__________________________________________________________________||
class MockDeliveryMethod(object):
    def __init__(self):
        self.results = None

    def deliver(self, results):
        self.results = results

##__________________________________________________________________||
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
MockArgs = collections.namedtuple('MockArgs', 'name')

##__________________________________________________________________||
class TestCollector(unittest.TestCase):

    def setUp(self):

        self.result = MockResult('result1')
        self.resultsCombinationMethod = MockResultsCombinationMethod(self.result)
        self.deliveryMethod = MockDeliveryMethod()
        self.obj = Collector(self.resultsCombinationMethod, self.deliveryMethod)

    def test_repr(self):
        repr(self.obj)

    def test_collect(self):

        args = MockArgs('args1')
        self.assertIs(self.result, self.obj.collect(args))
        self.assertIs(args, self.resultsCombinationMethod.args)
        self.assertIs(self.result, self.deliveryMethod.results)

##__________________________________________________________________||
