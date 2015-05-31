from AlphaTwirl.EventReader import EventReaderCollectorAssociatorComposite
import unittest

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name

##__________________________________________________________________||
class MockCollector(object): pass

##__________________________________________________________________||
class MockCollectorComposite(object):
    def __init__(self):
        self.added = [ ]

    def add(self, collector):
        self.added.append(collector)

##__________________________________________________________________||
class MockAssociator(object):
    def __init__(self):
        self.reader = None
        self.collector = MockCollector()

    def make(self, name):
        self.reader = MockReader(name)
        return self.reader

##__________________________________________________________________||
class TestEventReaderCollectorAssociatorComposite(unittest.TestCase):

    def test_associators_add_and_make(self):

        associatorComposite = EventReaderCollectorAssociatorComposite()
        collectorComposite = MockCollectorComposite()
        associatorComposite.collector = collectorComposite

        associator1 = MockAssociator()
        associatorComposite.add(associator1)
        self.assertIs(associator1.collector, collectorComposite.added[0])

        associator2 = MockAssociator()
        associatorComposite.add(associator2)
        self.assertIs(associator2.collector, collectorComposite.added[1])

        actual = associatorComposite.make("compName1") # need to evaluate actual before expected.
        expected = [associator1.reader, associator2.reader]
        self.assertEqual(expected, actual.readers)

        actual = associatorComposite.make("compName2")
        expected = [associator1.reader, associator2.reader]
        self.assertEqual(expected, actual.readers)

##__________________________________________________________________||
