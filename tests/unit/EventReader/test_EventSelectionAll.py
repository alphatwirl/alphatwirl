from AlphaTwirl.EventReader import EventSelectionAll
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

##__________________________________________________________________||
