from AlphaTwirl.EventReader import EventSelectionAll
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
class TestEventSelectionAll(unittest.TestCase):

    def test_true(self):
        selection = EventSelectionAll()
        selection.add(ReturnTrue())
        selection.add(ReturnTrue())
        selection.add(ReturnTrue())
        self.assertTrue(selection(MockEvent()))

    def test_false(self):
        selection = EventSelectionAll()
        selection.add(ReturnTrue())
        selection.add(ReturnTrue())
        selection.add(ReturnTrue())
        selection.add(ReturnFalse())
        self.assertFalse(selection(MockEvent()))

##____________________________________________________________________________||
