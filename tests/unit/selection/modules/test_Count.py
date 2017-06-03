# Tai Sakuma <tai.sakuma@cern.ch>
import unittest
import copy

from alphatwirl.selection.modules.Count import Count

##__________________________________________________________________||
class MockEventSelection(object):
    def __init__(self, name = None):
        self.name = name

##__________________________________________________________________||
class Test_Count(unittest.TestCase):

    def test_copy(self):
        obj = Count()
        obj._results[:] = [[1, 'class', 'name', 2, 3]]
        obj1 = obj.copy()
        self.assertIsNot(obj, obj1)
        self.assertIsNot(obj._results, obj1._results)
        self.assertEqual([[1, 'class', 'name', 2, 3]], obj1._results)

    def test_increment_depth(self):
        obj = Count()
        obj._results[:] = [
            [1, 'class1', 'name1', 6, 8],
            [1, 'class1', 'name2', 3, 6],
            [1, 'class2', 'name3', 1, 3],
        ]

        obj.increment_depth(by = 1)

        self.assertEqual(
            [
            [2, 'class1', 'name1', 6, 8],
            [2, 'class1', 'name2', 3, 6],
            [2, 'class2', 'name3', 1, 3],
            ],
            obj._results
        )

    def test_insert(self):
        obj = Count()
        obj._results[:] = [
            [1, 'class1', 'name1', 6, 8],
            [1, 'class1', 'name2', 3, 6],
            [1, 'class2', 'name3', 1, 3],
        ]

        obj1 = Count()
        obj1._results[:] = [
            [2, 'class2', 'name4', 4, 6],
            [2, 'class3', 'name5', 3, 4],
        ]

        obj.insert(1, obj1)

        self.assertEqual(
            [
                [1, 'class1', 'name1', 6, 8],
                [1, 'class1', 'name2', 3, 6],
                [2, 'class2', 'name4', 4, 6],
                [2, 'class3', 'name5', 3, 4],
                [1, 'class2', 'name3', 1, 3],
            ],
            obj._results
        )

    def test_insert_at_end(self):
        obj = Count()
        obj._results[:] = [
            [1, 'class1', 'name1', 6, 8],
            [1, 'class1', 'name2', 3, 6],
            [1, 'class2', 'name3', 1, 3],
        ]

        obj1 = Count()
        obj1._results[:] = [
            [2, 'class2', 'name4', 2, 3],
            [2, 'class3', 'name5', 1, 2],
        ]

        obj.insert(2, obj1)

        self.assertEqual(
            [
                [1, 'class1', 'name1', 6, 8],
                [1, 'class1', 'name2', 3, 6],
                [1, 'class2', 'name3', 1, 3],
                [2, 'class2', 'name4', 2, 3],
                [2, 'class3', 'name5', 1, 2],
            ],
            obj._results
        )

    def test_empty(self):
        obj = Count()
        obj.count(pass_ = [ ])

    def test_one(self):
        obj = Count()
        sel1 = MockEventSelection(name = 'sel1')
        obj.add(sel1)

        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 0, 0],
            ],
            obj._results
        )

        obj.count(pass_ = [True])
        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 1, 1],
            ],
            obj._results
        )

        obj.count(pass_ = [False])
        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 1, 2],
            ],
            obj._results
        )

    def test_three(self):
        obj = Count()
        sel1 = MockEventSelection(name = 'sel1')
        sel2 = MockEventSelection(name = 'sel2')
        sel3 = MockEventSelection()
        obj.add(sel1)
        obj.add(sel2)
        obj.add(sel3)

        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 0, 0],
                [1, 'MockEventSelection', 'sel2', 0, 0],
                [1, 'MockEventSelection',     '', 0, 0],
            ],
            obj._results
        )

        obj.count(pass_ = [True, False])
        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 1, 1],
                [1, 'MockEventSelection', 'sel2', 0, 1],
                [1, 'MockEventSelection',     '', 0, 0],
            ],
            obj._results
        )

        obj.count(pass_ = [True, True, False])
        self.assertEqual(
            [
                [1, 'MockEventSelection', 'sel1', 2, 2],
                [1, 'MockEventSelection', 'sel2', 1, 2],
                [1, 'MockEventSelection',     '', 0, 1],
            ],
            obj._results
        )

    def test_to_tuple_list(self):
        obj = Count()
        obj._results[:] = [
            [1, 'class1', 'name1', 6, 8],
            [1, 'class1', 'name2', 3, 6],
            [1, 'class2', 'name3', 1, 3],
        ]
        self.assertEqual(
            [
                (1, 'class1', 'name1', 6, 8),
                (1, 'class1', 'name2', 3, 6),
                (1, 'class2', 'name3', 1, 3)
            ], obj.to_tuple_list())

##__________________________________________________________________||
class TestCount_operator(unittest.TestCase):

    def setUp(self):

        self.obj1_results_org = [
            [1, 'class1', 'name1', 2, 2],
            [1, 'class1', 'name2', 1, 2],
            [1, 'class2', 'name3', 0, 1],
            ]
        self.obj1 = Count()
        self.obj1._results = copy.deepcopy(self.obj1_results_org)

        self.obj2_results_org = [
            [1, 'class1', 'name1', 3, 5],
            [1, 'class1', 'name2', 2, 4],
            [1, 'class2', 'name3', 1, 2],
        ]
        self.obj2 = Count()
        self.obj2._results = copy.deepcopy(self.obj2_results_org)

        self.expected = [
            [1, 'class1', 'name1', 5, 7],
            [1, 'class1', 'name2', 3, 6],
            [1, 'class2', 'name3', 1, 3],
            ]

    def test_add(self):

        obj3 = self.obj1 + self.obj2
        self.assertEqual(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results, obj3._results)
        self.assertIsNot(self.obj2._results, obj3._results)

        self.assertIsNot(self.obj1_results_org, self.obj1._results)
        self.assertEqual(self.obj1_results_org, self.obj1._results)

        self.assertIsNot(self.obj2_results_org, self.obj2._results)
        self.assertEqual(self.obj2_results_org, self.obj2._results)

    def test_radd(self):
        obj3 = sum([self.obj1, self.obj2]) # 0 + obj1 is executed
        self.assertEqual(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results, obj3._results)
        self.assertIsNot(self.obj2._results, obj3._results)

        self.assertIsNot(self.obj1_results_org, self.obj1._results)
        self.assertEqual(self.obj1_results_org, self.obj1._results)

        self.assertIsNot(self.obj2_results_org, self.obj2._results)
        self.assertEqual(self.obj2_results_org, self.obj2._results)

    def test_iadd(self):
        obj1 = self.obj1

        self.obj1 += self.obj2
        self.assertIs(self.obj1, obj1)
        self.assertEqual(self.expected, self.obj1._results)

        self.assertIsNot(self.obj1_results_org, self.obj1._results)

        self.assertIsNot(self.obj2_results_org, self.obj2._results)
        self.assertEqual(self.obj2_results_org, self.obj2._results)

    @unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
    def test_add_incompatible_different_length(self):
        obj2 = Count()
        obj2._results  = [
            [1, 'class1', 'name1', 3, 5],
            [1, 'class1', 'name2', 2, 4],
        ]
        obj3 = self.obj1 + obj2
        self.assertEqual(self.obj1._results, obj3._results)

    @unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
    def test_add_incompatible_different_first_values(self):
        obj2 = Count()
        obj2._results  = [
            [1, 'class1', 'name1', 3, 5],
            [1, 'class1', 'name2', 2, 4],
            [1, 'class2', 'name4', 1, 2],
        ]
        obj3 = self.obj1 + obj2
        self.assertEqual(self.obj1._results, obj3._results)

##__________________________________________________________________||
