import unittest

from .mock import MockSummarizer

##__________________________________________________________________||
class TestMockSummarizer(unittest.TestCase):

    def setUp(self):
        self.obj1 = MockSummarizer((1, 2))
        self.obj2 = MockSummarizer((3, 4))

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj1)

    def test_add(self):
        obj3 = self.obj1 + self.obj2
        self.assertEqual((1, 2, 3, 4), obj3._results)

    def test_radd(self):
        obj3 = sum([self.obj1, self.obj2])
        self.assertEqual((1, 2, 3, 4), obj3._results)

    def test_to_tuple_list(self):
        self.assertEqual((1, 2), self.obj1.to_tuple_list())

##__________________________________________________________________||
