from AlphaTwirl import EventReaderBundle
import unittest


##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class MockEventBuilder(object):
    def build(self, component):
        return component._events

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name
        self._events = [ ]

    def event(self, event):
        self._events.append(event)

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
        self.bundle = EventReaderBundle(self.eventBuilder)

    def test_addReaderPackage(self):
        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

    def test_begin(self):
        self.bundle.begin()

    def test_OneComponent_OnePackage(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent()
        event2 = MockEvent()
        event3 = MockEvent()
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        self.assertEqual(1, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)
        self.assertEqual([event1, event2, event3], package1._readers[0]._events)

        self.assertFalse(package1.collected)
        self.bundle.end()
        self.assertTrue(package1.collected)

    def test_OneComponent_TwoPackages(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent()
        event2 = MockEvent()
        event3 = MockEvent()
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        self.assertEqual(1, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)
        self.assertEqual([event1, event2, event3], package1._readers[0]._events)

        self.assertEqual(1, len(package2._readers))
        self.assertEqual("compName1", package2._readers[0].name)
        self.assertEqual([event1, event2, event3], package2._readers[0]._events)

        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        self.bundle.end()
        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)

    def test_TwoComponents_OnePackage(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent()
        event2 = MockEvent()
        event3 = MockEvent()
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        component2 = MockComponent()
        component2.name = "compName2"
        event11 = MockEvent()
        event12 = MockEvent()
        event13 = MockEvent()
        component2._events = [event11, event12, event13]
        self.bundle.read(component2)

        self.assertEqual(2, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)
        self.assertEqual([event1, event2, event3], package1._readers[0]._events)
        self.assertEqual("compName2", package1._readers[1].name)
        self.assertEqual([event11, event12, event13], package1._readers[1]._events)

        self.assertFalse(package1.collected)
        self.bundle.end()
        self.assertTrue(package1.collected)

    def test_TwoComponents_TwoPackages(self):

        package1 = MockReaderPackage()
        self.bundle.addReaderPackage(package1)

        package2 = MockReaderPackage()
        self.bundle.addReaderPackage(package2)

        component1 = MockComponent()
        component1.name = "compName1"
        event1 = MockEvent()
        event2 = MockEvent()
        event3 = MockEvent()
        component1._events = [event1, event2, event3]
        self.bundle.read(component1)

        component2 = MockComponent()
        component2.name = "compName2"
        event11 = MockEvent()
        event12 = MockEvent()
        event13 = MockEvent()
        component2._events = [event11, event12, event13]
        self.bundle.read(component2)

        self.assertEqual(2, len(package1._readers))
        self.assertEqual("compName1", package1._readers[0].name)
        self.assertEqual([event1, event2, event3], package1._readers[0]._events)
        self.assertEqual("compName2", package1._readers[1].name)
        self.assertEqual([event11, event12, event13], package1._readers[1]._events)

        self.assertEqual(2, len(package2._readers))
        self.assertEqual("compName1", package2._readers[0].name)
        self.assertEqual([event1, event2, event3], package2._readers[0]._events)
        self.assertEqual("compName2", package2._readers[1].name)
        self.assertEqual([event11, event12, event13], package2._readers[1]._events)

        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        self.bundle.end()
        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)

##____________________________________________________________________________||
