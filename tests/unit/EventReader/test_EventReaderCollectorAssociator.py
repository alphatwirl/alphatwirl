from AlphaTwirl.EventReader import EventReaderCollectorAssociator
import unittest

##____________________________________________________________________________||
class MockReader(object):
    pass

##____________________________________________________________________________||
class MockCollector(object):
    def __init__(self):
        self.readers = [ ]
        self.collected = False

    def addReader(self, datasetName, reader):
        self.readers.append((datasetName, reader))

    def collect(self):
        self.collected = True

##____________________________________________________________________________||
class TestEventReaderCollectorAssociator(unittest.TestCase):

    def test_make(self):
        collector = MockCollector()
        package = EventReaderCollectorAssociator(MockReader, collector)

        reader = package.make("data1")
        self.assertIsInstance(reader, MockReader)

        self.assertEqual([("data1", reader)], collector.readers)

    def test_collect(self):
        collector = MockCollector()
        package = EventReaderCollectorAssociator(MockReader, collector)

        self.assertFalse(collector.collected)
        package.collect()
        self.assertTrue(collector.collected)

    def test_no_collector(self):
        package = EventReaderCollectorAssociator(MockReader)
        package.collect()

##____________________________________________________________________________||
