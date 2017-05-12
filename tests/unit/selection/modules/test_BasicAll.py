# Tai Sakuma <tai.sakuma@cern.ch>
from alphatwirl.selection.modules import All
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class MockEventSelection(object):
    def __init__(self):
        self.isBeginCalled = False
        self.isEndCalled = False
        self.ret = True

    def begin(self, event):
        self.isBeginCalled = True

    def __call__(self, event):
        return self.ret

    def end(self):
        self.isEndCalled = True

##__________________________________________________________________||
class Test_All(unittest.TestCase):

    def test_empty(self):
        obj = All()

        event = MockEvent()
        self.assertTrue(obj(event))

    def test_standard(self):
        obj = All()
        selection1 = MockEventSelection()
        selection2 = MockEventSelection()

        obj.add(selection1)
        obj.add(selection2)

        self.assertFalse(selection1.isBeginCalled)
        self.assertFalse(selection2.isBeginCalled)

        self.assertFalse(selection1.isEndCalled)
        self.assertFalse(selection2.isEndCalled)

        event = MockEvent()
        obj.begin(event)
        self.assertTrue(selection1.isBeginCalled)
        self.assertTrue(selection2.isBeginCalled)

        event = MockEvent()
        selection1.ret = True
        selection2.ret = True
        self.assertTrue(obj(event))

        event = MockEvent()
        selection1.ret = True
        selection2.ret = False
        self.assertFalse(obj(event))

        event = MockEvent()
        selection1.ret = False
        selection2.ret = True
        self.assertFalse(obj.event(event))

        event = MockEvent()
        selection1.ret = False
        selection2.ret = False
        self.assertFalse(obj.event(event))

        obj.end()
        self.assertTrue(selection1.isEndCalled)
        self.assertTrue(selection2.isEndCalled)

##__________________________________________________________________||
