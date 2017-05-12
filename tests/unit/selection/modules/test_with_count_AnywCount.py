# Tai Sakuma <tai.sakuma@cern.ch>
from alphatwirl.selection.modules import AnywCount
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
class Test_AnywCount(unittest.TestCase):

    def test_empty(self):
        obj = AnywCount()

        event = MockEvent()
        obj.begin(event)

        event = MockEvent()
        self.assertFalse(obj(event))

        count = obj.results()
        self.assertEqual([ ], count._results)

    def test_standard(self):
        obj = AnywCount()
        sel1 = MockEventSelection(name = 'sel1')
        sel2 = MockEventSelection()

        obj.add(sel1)
        obj.add(sel2)

        self.assertFalse(sel1.is_begin_called)
        self.assertFalse(sel2.is_begin_called)

        self.assertFalse(sel1.is_end_called)
        self.assertFalse(sel2.is_end_called)

        event = MockEvent()
        obj.begin(event)
        self.assertTrue(sel1.is_begin_called)
        self.assertTrue(sel2.is_begin_called)

        event = MockEvent()
        sel1.ret = True   # 1/1
        sel2.ret = True   # 0/0
        self.assertTrue(obj(event))

        event = MockEvent()
        sel1.ret = True   # 2/2
        sel2.ret = False  # 0/0
        self.assertTrue(obj(event))

        event = MockEvent()
        sel1.ret = False  # 2/3
        sel2.ret = True   # 1/1
        self.assertTrue(obj.event(event))

        event = MockEvent()
        sel1.ret = False  # 2/4
        sel2.ret = False  # 1/2
        self.assertFalse(obj.event(event))

        obj.end()
        self.assertTrue(sel1.is_end_called)
        self.assertTrue(sel2.is_end_called)

        count = obj.results()
        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 2, 4],
                [1, 'MockEventSelection',     '', 1, 2],
            ],
            count._results
        )

    def test_nested(self):
        #
        # any (obj) --- any (obj1) --- sel (sel11)
        #            |              +- sel (sel12)
        #            +- any (obj2) --- sel (sel21)
        #            |              +- sel (sel22)
        #            +- sel (sel3)
        #

        obj = AnywCount()
        obj1 = AnywCount('all1')
        obj2 = AnywCount('all2')
        sel3 = MockEventSelection('sel3')
        sel11 = MockEventSelection('sel11')
        sel12 = MockEventSelection('sel12')
        sel21 = MockEventSelection('sel21')
        sel22 = MockEventSelection('sel22')
        obj.add(obj1)
        obj.add(obj2)
        obj.add(sel3)
        obj1.add(sel11)
        obj1.add(sel12)
        obj2.add(sel21)
        obj2.add(sel22)

        self.assertFalse(sel11.is_begin_called)
        self.assertFalse(sel12.is_begin_called)
        self.assertFalse(sel21.is_begin_called)
        self.assertFalse(sel22.is_begin_called)
        self.assertFalse(sel3.is_begin_called)

        self.assertFalse(sel11.is_end_called)
        self.assertFalse(sel12.is_end_called)
        self.assertFalse(sel21.is_end_called)
        self.assertFalse(sel22.is_end_called)
        self.assertFalse(sel3.is_end_called)

        event = MockEvent()
        obj.begin(event)
        self.assertTrue(sel11.is_begin_called)
        self.assertTrue(sel12.is_begin_called)
        self.assertTrue(sel21.is_begin_called)
        self.assertTrue(sel22.is_begin_called)
        self.assertTrue(sel3.is_begin_called)

        event = MockEvent()
        sel11.ret = True   # 1/1
        sel12.ret = True   # 1/1
        sel21.ret = True   # 1/1
        sel22.ret = True   # 1/1
        sel3.ret = True    # 1/1
        self.assertTrue(obj(event))

        obj.end()
        self.assertTrue(sel11.is_end_called)
        self.assertTrue(sel12.is_end_called)
        self.assertTrue(sel21.is_end_called)
        self.assertTrue(sel22.is_end_called)
        self.assertTrue(sel3.is_end_called)

        count = obj.results()
        self.assertEqual(
            [
                [1, 'AnywCount', 'all1',  1, 1],
                [2, 'MockEventSelection',     'sel11', 1, 1],
                [2, 'MockEventSelection',     'sel12', 0, 0],
                [1, 'AnywCount', 'all2',  0, 0],
                [2, 'MockEventSelection',     'sel21', 0, 0],
                [2, 'MockEventSelection',     'sel22', 0, 0],
                [1, 'MockEventSelection',     'sel3',  0, 0],
            ],
            count._results
        )

##__________________________________________________________________||
