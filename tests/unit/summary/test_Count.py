import unittest

import copy
import numpy as np

from alphatwirl.summary import Count

##__________________________________________________________________||
class TestCount(unittest.TestCase):

    def test_init(self):
        obj = Count()
        np.testing.assert_equal([np.array([0, 0])], obj.contents)

    def test_init_val(self):
        obj = Count(val = ())
        np.testing.assert_equal([np.array([1, 1])], obj.contents)

    def test_init_weight(self):
        obj = Count(val = (), weight = 10)
        np.testing.assert_equal([np.array([10, 100])], obj.contents)

    def test_init_contents(self):
        obj = Count(contents = [np.array([1, 3])])
        np.testing.assert_equal([np.array([1, 3])], obj.contents)

    @unittest.skip("they are the same object now")
    def test_init_contents_not_same_object(self):
        contents = [np.array([1, 3])]
        obj = Count(contents = contents)
        np.testing.assert_equal(contents, obj.contents)
        self.assertIsNot(contents, obj.contents)
        self.assertIsNot(contents[0], obj.contents[0])

    def test_repr(self):
        obj = Count()
        repr(obj)

    def test_add(self):
        obj1 = Count(contents = [np.array((10, 20))])
        obj2 = Count(contents = [np.array((30, 40))])
        obj3 =  obj1 + obj2
        np.testing.assert_equal([np.array([40, 60])], obj3.contents)
        self.assertIsNot(obj1, obj3)
        self.assertIsNot(obj1.contents, obj3.contents)
        self.assertIsNot(obj2, obj3)
        self.assertIsNot(obj2.contents, obj3.contents)

    def test_radd(self):
        obj1 = Count(contents = [np.array((10, 20))])
        self.assertIsNot(obj1, sum([obj1])) # will call 0 + obj1
        self.assertEqual(obj1, sum([obj1]))

    def test_radd_raise(self):
        obj1 = Count(contents = [np.array((10, 20))])
        self.assertRaises(TypeError, obj1.__radd__, 1)

    def test_copy(self):
        obj1 = Count(contents = [np.array((10, 20))])
        copy1 = copy.copy(obj1)
        self.assertEqual(obj1, copy1)
        self.assertIsNot(obj1, copy1)
        self.assertIsNot(obj1.contents, copy1.contents)
        self.assertIsNot(obj1.contents[0], copy1.contents[0])

##__________________________________________________________________||
