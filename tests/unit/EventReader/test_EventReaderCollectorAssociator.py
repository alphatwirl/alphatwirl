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

##____________________________________________________________________________||
class TestEventReaderCollectorAssociator(unittest.TestCase):

    def test_make(self):
        collector = MockCollector()
        associator = EventReaderCollectorAssociator(MockReader, collector)

        reader = associator.make("data1")
        self.assertIsInstance(reader, MockReader)

        self.assertEqual([("data1", reader)], collector.readers)

##____________________________________________________________________________||
