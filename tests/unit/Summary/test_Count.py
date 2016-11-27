import unittest
import numpy as np

from AlphaTwirl.Summary import Count

##__________________________________________________________________||
class TestCount(unittest.TestCase):

    def test_init(self):
        obj = Count()
        np.testing.assert_equal(np.array([1, 1]), obj.contents)

    def test_init_weight(self):
        obj = Count(weight = 10)
        np.testing.assert_equal(np.array([10, 100]), obj.contents)

    def test_init_contents(self):
        obj = Count(contents = (1, 3))
        np.testing.assert_equal(np.array([1, 3]), obj.contents)

    def test_init_contents_not_same_object(self):
        contents = np.array([1, 3])
        obj = Count(contents = contents)
        np.testing.assert_equal(contents, obj.contents)
        self.assertIsNot(contents, obj.contents)

    def test_add(self):
        obj1 = Count(contents = (10, 20))
        obj2 = Count(contents = (30, 40))
        obj3 =  obj1 + obj2
        np.testing.assert_equal(np.array([40, 60]), obj3.contents)
        self.assertIsNot(obj1, obj3)
        self.assertIsNot(obj1.contents, obj3.contents)
        self.assertIsNot(obj2, obj3)
        self.assertIsNot(obj2.contents, obj3.contents)
##__________________________________________________________________||
