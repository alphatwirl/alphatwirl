import unittest
import numpy as np

from AlphaTwirl.Summary import Count

##__________________________________________________________________||
class TestCount(unittest.TestCase):

    def assert_np_dict_frame(self, f1, f2):
        self.assertEqual(sorted(f1.keys()), sorted(f2.keys()))
        for k in sorted(f1.keys()):
            np.testing.assert_equal(f1[k], f2[k])

    def test_add(self):
        obj = Count()

        obj.add(1)
        expected  = {1: np.array((1, 1))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(1)
        expected  = {1: np.array((2, 2))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(1, weight = 2)
        expected  = {1: np.array((4, 6))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(2, weight = 3.2)
        expected  = {
            1: np.array((4, 6)),
            2: np.array((3.2, 3.2**2)),
        }
        self.assert_np_dict_frame(expected, obj.results())
        # self.assertEqual(expected, obj.results()) # this doesn't work

    def test_add_key(self):
        counts = Count()
        counts.add_key(1)
        expected  = {1: np.array((0, 0))}
        self.assert_np_dict_frame(expected, counts.results())

        counts.add_key(3)
        counts.add_key(5)
        expected  = {
            1: np.array((0, 0)),
            3: np.array((0, 0)),
            5: np.array((0, 0))
        }
        self.assert_np_dict_frame(expected, counts.results())

    def test_copy_from(self):
        obj = Count()
        src_obj = Count()

        expected  = {
            10: np.array((24.0, 3.0)),
            20: np.array((33.0, 5.0)),
            30: np.array((21.0, 4.0)),
            }

        src_obj._results.update(expected)
        obj.copy_from(src_obj)
        self.assertEqual(expected, src_obj.results()) # don't know why assertEqual() works
        self.assertIsNot(obj._results, src_obj._results)

##__________________________________________________________________||
class TestCount_operator(unittest.TestCase):

    def assert_np_dict_frame(self, f1, f2):
        self.assertEqual(sorted(f1.keys()), sorted(f2.keys()))
        for k in sorted(f1.keys()):
            np.testing.assert_equal(f1[k], f2[k])

    def setUp(self):
        self.obj1 = Count()
        self.obj2 = Count()

        self.obj1._results  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)), # int
            (3, ): np.array((2, 3)),
            }

        self.obj2._results  = {
            (2, ): np.array((3.2, 6.1)), # add float to int
            (4, ): np.array((  2,   2)),
        }

        self.expected = {
            (1, ): np.array((  4,    6)),
            (2, ): np.array((6.2, 15.1)),
            (3, ): np.array((  2,    3)),
            (4, ): np.array((  2,    2)),
            }

    def test_add(self):
        obj3 = self.obj1 + self.obj2
        self.assert_np_dict_frame(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results[(1, )], obj3._results[(1, )])
        self.assertIsNot(self.obj2._results[(4, )], obj3._results[(4, )])

    def test_radd(self):
        obj3 = sum([self.obj1, self.obj2]) # 0 + obj1 is executed
        self.assert_np_dict_frame(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results[(1, )], obj3._results[(1, )])
        self.assertIsNot(self.obj2._results[(4, )], obj3._results[(4, )])

    def test_iadd(self):
        obj1 = self.obj1

        self.obj1 += self.obj2
        self.assertIs(self.obj1, obj1)
        self.assert_np_dict_frame(self.expected, self.obj1._results)


##__________________________________________________________________||
