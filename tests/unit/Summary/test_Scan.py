import unittest
import numpy as np

from AlphaTwirl.Summary import Scan

##__________________________________________________________________||
class TestScan(unittest.TestCase):

    def assert_np_dict_frame(self, f1, f2):
        self.assertEqual(sorted(f1.keys()), sorted(f2.keys()))
        for k in sorted(f1.keys()):
            np.testing.assert_equal(f1[k], f2[k])

    def test_add_simple(self):
        obj = Scan(n = 3)

        obj.add((1, 2), (10, 20))
        expected  = [(1, 2, 10, 20)]
        self.assertEqual(expected, obj.results())

        obj.add((1, 3), (15, 22))
        expected  = [
            (1, 2, 10, 20),
            (1, 3, 15, 22)
            ]
        self.assertEqual(expected, obj.results())

        obj.add((3, 5), (35, 42), weight = 2)
        expected  = [
            (1, 2, 10, 20),
            (1, 3, 15, 22),
            (3, 5, 35, 42)
            ]
        self.assertEqual(expected, obj.results())

        obj.add((5, 8), (55, 41)) # the 4th time, don't add because n = 3
        expected  = [
            (1, 2, 10, 20),
            (1, 3, 15, 22),
            (3, 5, 35, 42)
            ]
        self.assertEqual(expected, obj.results())

    def test_add_key(self):
        obj = Scan()
        obj.add_key((1, 2)) # does nothing
        expected  = [ ] #
        self.assertEqual(expected, obj.results())

    def test_copy_from(self):
        obj = Scan()
        src_obj = Scan()

        expected  = [
            (1, 2, 10, 20),
            (1, 3, 15, 22),
            (3, 5, 35, 42)
            ]

        src_obj._results = expected
        obj.copy_from(src_obj)
        self.assertEqual(expected, src_obj.results()) # don't know why assertEqual() works
        self.assertIsNot(obj._results, src_obj._results)

##__________________________________________________________________||
class TestScan_operator(unittest.TestCase):

    def setUp(self):
        self.obj1 = Scan()
        self.obj2 = Scan()

        self.obj1._results  = [
            (1, 2, 10, 20),
            (1, 3, 15, 22),
            (3, 5, 35, 42)
            ]

        self.obj2._results  = [
            (4, 8, 30, 80),
            (5, 6, 45, 92),
        ]

        self.expected = [
            (1, 2, 10, 20),
            (1, 3, 15, 22),
            (3, 5, 35, 42),
            (4, 8, 30, 80),
            (5, 6, 45, 92),
            ]

    def test_add(self):
        obj3 = self.obj1 + self.obj2
        self.assertEqual(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results, obj3._results)
        self.assertIsNot(self.obj2._results, obj3._results)

    def test_radd(self):
        obj3 = sum([self.obj1, self.obj2]) # 0 + obj1 is executed
        self.assertEqual(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results, obj3._results)
        self.assertIsNot(self.obj2._results, obj3._results)

    def test_iadd(self):
        obj1 = self.obj1

        self.obj1 += self.obj2
        self.assertIs(self.obj1, obj1)
        self.assertEqual(self.expected, self.obj1._results)


##__________________________________________________________________||
