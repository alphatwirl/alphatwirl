import unittest
import numpy as np

from AlphaTwirl.Counter import Count

##__________________________________________________________________||
class TestCount(unittest.TestCase):

    def assert_np_dict_frame(self, f1, f2):
        self.assertEqual(sorted(f1.keys()), sorted(f2.keys()))
        for k in sorted(f1.keys()):
            np.testing.assert_equal(f1[k], f2[k])

    def test_count(self):
        obj = Count()

        obj.count(1)
        expected  = {1: np.array((1, 1))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.count(1)
        expected  = {1: np.array((2, 2))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.count(1, weight = 2)
        expected  = {1: np.array((4, 6))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.count(2, weight = 3)
        expected  = {
            1: np.array((4, 6)),
            2: np.array((3, 9)),
        }
        self.assert_np_dict_frame(expected, obj.results())
        # self.assertEqual(expected, obj.results()) # this doesn't work

    def test_copyFrom(self):
        obj = Count()
        src_obj = Count()

        expected  = {
            10: np.array((24.0, 3.0)),
            20: np.array((33.0, 5.0)),
            30: np.array((21.0, 4.0)),
            }

        src_obj._results.update(expected)
        obj.copyFrom(src_obj)
        self.assertEqual(expected, src_obj.results()) # don't know why this works
        self.assertIsNot(obj._results, src_obj._results)

    def test_addKey(self):
        counts = Count()
        counts.addKey(1)
        expected  = {1: np.array((0, 0))}
        self.assert_np_dict_frame(expected, counts.results())

        counts.addKey(3)
        counts.addKey(5)
        expected  = {
            1: np.array((0, 0)),
            3: np.array((0, 0)),
            5: np.array((0, 0))
        }
        self.assert_np_dict_frame(expected, counts.results())

##__________________________________________________________________||
