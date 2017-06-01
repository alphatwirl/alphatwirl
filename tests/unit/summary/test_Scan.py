import unittest

import copy
import numpy as np

from alphatwirl.summary import Scan

##__________________________________________________________________||
class TestScan(unittest.TestCase):

    def test_init(self):
        obj = Scan()
        np.testing.assert_equal([ ], obj.contents)

    def test_init_val(self):
        obj = Scan(val = (10, 20))
        self.assertEqual([(10, 20)], obj.contents)

    def test_init_weight(self): # no effect
        obj = Scan(val = (10, 20), weight = 2)
        self.assertEqual([(10, 20)], obj.contents)

    def test_init_contents(self):
        obj = Scan(contents = [(10, 20), (30, 40)])
        self.assertEqual([(10, 20), (30, 40)], obj.contents)

    @unittest.skip("they can be the same object now")
    def test_init_contents_not_same_object(self):
        contents = [[10, 20], [30, 40]]
        obj = Scan(contents = contents)
        self.assertIsNot(contents, obj.contents)
        self.assertIsNot(contents[0], obj.contents[0])
        self.assertIsNot(contents[1], obj.contents[1])

    def test_repr(self):
        obj = Scan()
        repr(obj)

    def test_add(self):
        obj1 = Scan(contents = [(10, 20), (30, 40)])
        obj2 = Scan(contents = [(50, 60), (70, 80)])
        obj3 =  obj1 + obj2
        self.assertEqual([(10, 20), (30, 40), (50, 60), (70, 80)], obj3.contents)
        self.assertIsNot(obj1, obj3)
        self.assertIsNot(obj1.contents, obj3.contents)
        self.assertIsNot(obj2, obj3)
        self.assertIsNot(obj2.contents, obj3.contents)

    def test_radd(self):
        obj1 = Scan(contents = [(10, 20), (30, 40)])
        self.assertIsNot(obj1, sum([obj1])) # will call 0 + obj1
        self.assertEqual(obj1, sum([obj1]))

    def test_radd_raise(self):
        obj1 = Scan(contents = [(10, 20), (30, 40)])
        self.assertRaises(TypeError, obj1.__radd__, 1)

    def test_copy(self):
        obj1 = Scan(contents = [(10, 20), (30, 40)])
        copy1 = copy.copy(obj1)
        self.assertEqual(obj1, copy1)
        self.assertIsNot(obj1, copy1)
        self.assertIsNot(obj1.contents, copy1.contents)

##__________________________________________________________________||
