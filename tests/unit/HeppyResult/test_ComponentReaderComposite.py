from alphatwirl.heppyresult import ComponentReaderComposite
import unittest

##__________________________________________________________________||
class MockReader:
    def __init__(self, ret):
        self.beginCalled = False
        self.readComponents = [ ]
        self.endCalled = False
        self.ret = ret
    def begin(self): self.beginCalled = True
    def read(self, component): self.readComponents.append(component)
    def end(self):
        self.endCalled = True
        return self.ret

##__________________________________________________________________||
class MockComponent: pass

##__________________________________________________________________||
class TestComponentReaderComposite(unittest.TestCase):

    def test_read(self):
        bundle = ComponentReaderComposite()

        reader1 = MockReader(1111)
        bundle.add(reader1)
        reader2 = MockReader(2222)
        bundle.add(reader2)

        self.assertFalse(reader1.beginCalled)
        self.assertEqual([ ], reader1.readComponents)
        self.assertFalse(reader1.endCalled)

        self.assertFalse(reader2.beginCalled)
        self.assertEqual([ ], reader2.readComponents)
        self.assertFalse(reader2.endCalled)

        component1 = MockComponent()
        component2 = MockComponent()

        bundle.begin()
        bundle.read(component1)
        bundle.read(component2)
        self.assertEqual([1111, 2222], bundle.end())

        self.assertTrue(reader1.beginCalled)
        self.assertTrue(reader2.beginCalled)
        self.assertEqual([component1, component2], reader1.readComponents)
        self.assertEqual([component1, component2], reader2.readComponents)
        self.assertTrue(reader1.endCalled)
        self.assertTrue(reader2.endCalled)

##__________________________________________________________________||
