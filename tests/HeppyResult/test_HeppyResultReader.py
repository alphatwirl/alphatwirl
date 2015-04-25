from AlphaTwirl.HeppyResult import HeppyResultReader
import unittest

##____________________________________________________________________________||
class MockReader:
    def __init__(self):
        self.beginCalled = False
        self.readComponents = [ ]
        self.endCalled = False
    def begin(self): self.beginCalled = True
    def read(self, component): self.readComponents.append(component)
    def end(self): self.endCalled = True

##____________________________________________________________________________||
class MockComponent: pass

##____________________________________________________________________________||
class MockHeppyResult:
    def __init__(self, components): self._components = components
    def components(self): return self._components

##____________________________________________________________________________||
class TestHeppyResultReader(unittest.TestCase):

    def test_read(self):
        reader = HeppyResultReader()

        subreader1 = MockReader()
        reader.addReader(subreader1)
        subreader2 = MockReader()
        reader.addReader(subreader2)

        self.assertFalse(subreader1.beginCalled)
        self.assertEqual([ ], subreader1.readComponents)
        self.assertFalse(subreader1.endCalled)

        self.assertFalse(subreader2.beginCalled)
        self.assertEqual([ ], subreader2.readComponents)
        self.assertFalse(subreader2.endCalled)

        component1 = MockComponent()
        component2 = MockComponent()
        heppyResult = MockHeppyResult([component1, component2])

        reader.read(heppyResult)

        self.assertTrue(subreader1.beginCalled)
        self.assertTrue(subreader2.beginCalled)
        self.assertEqual([component1, component2], subreader1.readComponents)
        self.assertEqual([component1, component2], subreader2.readComponents)
        self.assertTrue(subreader1.endCalled)
        self.assertTrue(subreader2.endCalled)

##____________________________________________________________________________||
