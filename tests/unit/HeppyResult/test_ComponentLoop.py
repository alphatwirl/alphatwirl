from AlphaTwirl.HeppyResult import ComponentLoop
import unittest

##____________________________________________________________________________||
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

##____________________________________________________________________________||
class MockComponent: pass

##____________________________________________________________________________||
class TestComponentLoop(unittest.TestCase):

    def test_read(self):
        reader = MockReader()
        componentLoop = ComponentLoop(reader)

        self.assertFalse(reader.beginCalled)
        self.assertEqual([ ], reader.readComponents)
        self.assertFalse(reader.endCalled)

        component1 = MockComponent()
        component2 = MockComponent()
        components = [component1, component2]

        self.assertEqual(2232, componentLoop(components))

        self.assertTrue(reader.beginCalled)
        self.assertEqual(components, reader.readComponents)
        self.assertTrue(reader.endCalled)

##____________________________________________________________________________||
