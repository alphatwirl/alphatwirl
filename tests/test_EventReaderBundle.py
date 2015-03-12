from AlphaTwirl import EventReaderBundle, EventLooperRunner
import unittest


##____________________________________________________________________________||
class MockEvent(object):
    def __init__(self, id):
        self.id = id

##____________________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##____________________________________________________________________________||
class MockReaderPackage(object):
    def __init__(self):
        self._readers = [ ]
        self.collected = False

    def make(self, name):
        reader = MockReader(name)
        self._readers.append(reader)
        return reader

    def collect(self):
        self.collected = True

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self):
        self._events = None

##____________________________________________________________________________||
class TestEventReaderEventReaderBundle(unittest.TestCase):

    def setUp(self):
        self.eventBuilder = MockEventBuilder()
        self.eventLooperRunner = EventLooperRunner()
        self.bundle = EventReaderBundle(self.eventBuilder, self.eventLooperRunner)

    def test_addReaderPackage(self):
        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

    def test_begin_end(self):
        self.bundle.begin()
        self.bundle.end()

    def test_OneComponent_OnePackage(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        self.bundle.begin()

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        self.assertEqual(1, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)

        self.assertFalse(package1.collected)
        self.bundle.end()
        self.assertEqual([event1.id, event2.id, event3.id], package1._readers[0]._eventIds)
        self.assertTrue(package1.collected)

    def test_OneComponent_TwoPackages(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

        self.bundle.begin()

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        self.assertEqual(1, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)

        self.assertEqual(1, len(package2._readers))
        self.assertEqual("compName1", package2._readers[0].name)

        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        self.bundle.end()

        self.assertEqual([event1.id, event2.id, event3.id], package1._readers[0]._eventIds)
        self.assertEqual([event1.id, event2.id, event3.id], package2._readers[0]._eventIds)

        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)

    def test_TwoComponents_OnePackage(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        self.bundle.begin()

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        component2 = MockComponent()
        component2.name = "compName2"
        event11 = MockEvent(201)
        event12 = MockEvent(202)
        event13 = MockEvent(203)
        component2._events = [event11, event12, event13]
        self.bundle.read(component2)

        self.assertEqual(2, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)
        self.assertEqual("compName2", package1._readers[1].name)

        self.assertFalse(package1.collected)
        self.bundle.end()

        self.assertEqual([event1.id, event2.id, event3.id], package1._readers[0]._eventIds)
        self.assertEqual([event11.id, event12.id, event13.id], package1._readers[1]._eventIds)
        self.assertTrue(package1.collected)

    def test_TwoComponents_TwoPackages(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

        self.bundle.begin()

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent(101)
        event2 = MockEvent(102)
        event3 = MockEvent(103)
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        component2 = MockComponent()
        component2.name = "compName2"
        event11 = MockEvent(201)
        event12 = MockEvent(202)
        event13 = MockEvent(203)
        component2._events = [event11, event12, event13]
        self.bundle.read(component2)

        self.assertEqual(2, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)
        self.assertEqual("compName2", package1._readers[1].name)

        self.assertEqual(2, len(package2._readers))
        self.assertEqual("compName1", package2._readers[0].name)
        self.assertEqual("compName2", package2._readers[1].name)

        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        self.bundle.end()

        self.assertEqual([event1.id, event2.id, event3.id], package1._readers[0]._eventIds)
        self.assertEqual([event11.id, event12.id, event13.id], package1._readers[1]._eventIds)
        self.assertEqual([event1.id, event2.id, event3.id], package2._readers[0]._eventIds)
        self.assertEqual([event11.id, event12.id, event13.id], package2._readers[1]._eventIds)

        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)

##____________________________________________________________________________||
