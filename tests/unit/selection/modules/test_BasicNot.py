# Tai Sakuma <tai.sakuma@cern.ch>
from alphatwirl.selection.modules import Not
import unittest

##__________________________________________________________________||
class MockEvent(object):
    def __init__(self, val):
        self.val = val

##__________________________________________________________________||
class MockEventSelection(object):
    def __init__(self):
        self.isBeginCalled = False
        self.isEndCalled = False

    def begin(self, event):
        self.isBeginCalled = True

    def __call__(self, event):
        return event.val

    def end(self):
        self.isEndCalled = True

##__________________________________________________________________||
class Test_Not(unittest.TestCase):

    def test_one(self):
        selection = MockEventSelection()
        obj = Not(selection)

        self.assertFalse(selection.isBeginCalled)
        self.assertFalse(selection.isEndCalled)

        event = MockEvent(True)
        obj.begin(event)
        self.assertTrue(selection.isBeginCalled)

        event = MockEvent(True)
        self.assertFalse(obj(event))

        event = MockEvent(False)
        self.assertTrue(obj(event))

        event = MockEvent(False)
        self.assertTrue(obj.event(event))

        obj.end()
        self.assertTrue(selection.isEndCalled)

##__________________________________________________________________||
