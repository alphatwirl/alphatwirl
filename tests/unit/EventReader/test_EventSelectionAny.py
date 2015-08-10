from AlphaTwirl.EventReader import EventSelectionAny
import unittest

##____________________________________________________________________________||
class ReturnTrue(object):
    def __call__(self, event):
        return True

##____________________________________________________________________________||
class ReturnFalse(object):
    def __call__(self, event):
        return False

##____________________________________________________________________________||
class MockEvent(object): pass

##____________________________________________________________________________||
class TestEventSelectionAny(unittest.TestCase):

    def test_true(self):
        selection = EventSelectionAny()
        selection.add(ReturnFalse())
        selection.add(ReturnFalse())
        selection.add(ReturnTrue())
        selection.add(ReturnFalse())
        self.assertTrue(selection(MockEvent()))

    def test_false(self):
        selection = EventSelectionAny()
        selection.add(ReturnFalse())
        selection.add(ReturnFalse())
        selection.add(ReturnFalse())
        selection.add(ReturnFalse())
        self.assertFalse(selection(MockEvent()))

##____________________________________________________________________________||
