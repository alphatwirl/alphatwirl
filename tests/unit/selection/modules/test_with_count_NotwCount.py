# Tai Sakuma <tai.sakuma@cern.ch>
from alphatwirl.selection.modules import NotwCount
import unittest

##__________________________________________________________________||
class MockEvent(object): pass

##__________________________________________________________________||
class MockEventSelection(object):
    def __init__(self, name = None):
        self.name = name
        self.is_begin_called = False
        self.is_end_called = False
        self.ret = True

    def begin(self, event):
        self.is_begin_called = True

    def __call__(self, event):
        return self.ret

    def end(self):
        self.is_end_called = True

##__________________________________________________________________||
class Test_NotwCount(unittest.TestCase):

    def test_standard(self):

        sel1 = MockEventSelection(name = 'sel1')
        obj = NotwCount(selection = sel1)

        self.assertFalse(sel1.is_begin_called)

        self.assertFalse(sel1.is_end_called)

        event = MockEvent()
        obj.begin(event)
        self.assertTrue(sel1.is_begin_called)

        event = MockEvent()
        sel1.ret = False   # 1/1
        self.assertTrue(obj(event))

        event = MockEvent()
        sel1.ret = True  # 1/2
        self.assertFalse(obj.event(event))

        obj.end()
        self.assertTrue(sel1.is_end_called)

        count = obj.results()
        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 1, 2],
            ],
            count._results
        )

##__________________________________________________________________||
