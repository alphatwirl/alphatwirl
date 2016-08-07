from AlphaTwirl.Loop import Collector
import unittest

##__________________________________________________________________||
class MockReader(object):
    pass

##__________________________________________________________________||
class MockMethod(object):
    def __init__(self):
        self.readers = None
    def collect(self, readers):
        self.readers = readers

##__________________________________________________________________||
class MockResultsCombinationMethod(object):
    def __init__(self):
        self.readers = None
    def combine(self, readers):
        self.readers = readers
        return 4234

##__________________________________________________________________||
class MockDeliveryMethod(object):
    def __init__(self):
        self.results = None
    def deliver(self, results):
        self.results = results

##__________________________________________________________________||
class TestCollector(unittest.TestCase):

    def test_collect(self):
        method = MockMethod()
        resultsCombinationMethod = MockResultsCombinationMethod()
        deliveryMethod = MockDeliveryMethod()
        collector = Collector(resultsCombinationMethod, deliveryMethod)

        reader1 = MockReader()
        collector.addReader('data1', reader1)

        reader2 = MockReader()
        collector.addReader('data2', reader2)

        self.assertIsNone(method.readers)
        self.assertIsNone(deliveryMethod.results)
        self.assertEqual(4234, collector.collect())
        self.assertEqual([('data1', reader1), ('data2', reader2)], resultsCombinationMethod.readers)
        self.assertEqual(4234, deliveryMethod.results)


##__________________________________________________________________||
