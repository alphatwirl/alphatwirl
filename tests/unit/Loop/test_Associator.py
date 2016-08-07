from AlphaTwirl.Loop import Associator
import unittest

##__________________________________________________________________||
class MockReader(object):
    def __init__(self):
        self.content = [ ]

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self):
        self.readers = [ ]

    def addReader(self, datasetName, reader):
        self.readers.append((datasetName, reader))

##__________________________________________________________________||
class TestAssociator(unittest.TestCase):

    def test_make(self):
        reader = MockReader()
        collector = MockCollector()
        associator = Associator(reader, collector)

        reader1 = associator.make("data1")

        self.assertIsNot(reader, reader1)
        self.assertIsNot(reader.content, reader1.content)
        self.assertIsInstance(reader1, MockReader)
        self.assertEqual([("data1", reader1)], collector.readers)

    def test_NullCollector(self):
        reader = MockReader()
        associator = Associator(reader)
        reader1 = associator.make("data1")

##__________________________________________________________________||
