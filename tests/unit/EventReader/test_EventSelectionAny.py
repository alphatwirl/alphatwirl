from AlphaTwirl.EventReader import EventSelectionAny
import unittest

##__________________________________________________________________||
class ReturnTrue(object):
    def __call__(self, event):
        return True

##__________________________________________________________________||
class ReturnFalse(object):
    def __call__(self, event):
        return False

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
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

##__________________________________________________________________||
