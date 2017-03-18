from alphatwirl.heppyresult import ComponentLoop
import unittest

##__________________________________________________________________||
class MockReader:
    def __init__(self):
        self.beginCalled = False
        self.readComponents = [ ]
        self.endCalled = False
    def begin(self): self.beginCalled = True
    def read(self, component): self.readComponents.append(component)
    def end(self):
        self.endCalled = True
        return 2232

##__________________________________________________________________||
class MockHeppyResult:
    def __init__(self, components):
        self._components = components
    def components(self): return self._components

##__________________________________________________________________||
class MockComponent: pass

##__________________________________________________________________||
class TestComponentLoop(unittest.TestCase):

    def test_read(self):
        reader = MockReader()

        self.assertFalse(reader.beginCalled)
        self.assertEqual([ ], reader.readComponents)
        self.assertFalse(reader.endCalled)

        component1 = MockComponent()
        component2 = MockComponent()
        components = [component1, component2]
        heppyResult = MockHeppyResult(components)

        componentLoop = ComponentLoop(heppyResult, reader)

        self.assertEqual(2232, componentLoop())

        self.assertTrue(reader.beginCalled)
        self.assertEqual(components, reader.readComponents)
        self.assertTrue(reader.endCalled)

##__________________________________________________________________||
