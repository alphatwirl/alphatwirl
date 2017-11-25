import unittest
import copy
import sys

import numpy as np

from alphatwirl.summary import Summarizer
from alphatwirl.summary import Sum

##__________________________________________________________________||
class TestSummarizer(unittest.TestCase):

    def test_init_repr(self):
        obj = Summarizer(Summary = Sum)
        repr(obj)

    def test_add(self):

        obj = Summarizer(Summary = Sum)

        obj.add('A', (12, ) )
        expected  = {'A': Sum(contents = np.array((12, )))}
        self.assertEqual(expected, obj.results())

        obj.add('A', (23, ))
        expected  = {'A': Sum(contents = np.array((35, )))}
        self.assertEqual(expected, obj.results())

        obj.add('A', (10, ), weight = 2)
        expected  = {'A': Sum(contents = np.array((55, )))}
        self.assertEqual(expected, obj.results())

        obj.add('B', (20, ), weight = 3.2)
        expected  = {
            'A': Sum(contents = np.array((55, ))),
            'B': Sum(contents = np.array((64.0, ))),
        }
        self.assertEqual(expected, obj.results())

        return

    def test_add_key(self):
        obj = Summarizer(Summary = Sum)
        obj.add_key('A')
        expected  = {'A': Sum(contents = np.array((0, )))}
        self.assertEqual(expected, obj.results())

        obj.add_key('B')
        obj.add_key('C')
        expected  = {
            'A': Sum(contents = np.array((0, ))),
            'B': Sum(contents = np.array((0, ))),
            'C': Sum(contents = np.array((0, ))),
        }
        self.assertEqual(expected, obj.results())

    def test_key(self):
        obj = Summarizer(Summary = Sum)
        obj.add_key('A')
        self.assertEqual(['A'], list(obj.keys()))

    def test_to_tuple_list(self):
        obj = Summarizer(Summary = Sum)
        obj.add(('A', ), (12, ))
        obj.add(('B', ), (20, ))
        self.assertEqual([('A', 12), ('B', 20)], obj.to_tuple_list())

    @unittest.skipUnless(sys.version_info[0] == 2, "skip for Python 3")
    def test_to_tuple_list_key_not_tuple(self):
        obj = Summarizer(Summary = Sum)
        obj.add('A', (12, )) # the keys are not a tuple
        obj.add(2, (20, ))   #
        self.assertEqual([(2, 20), ('A', 12)], obj.to_tuple_list())

##__________________________________________________________________||
class TestSummarizer_operator(unittest.TestCase):

    def setUp(self):
        self.obj1 = Summarizer(Summary = Sum)
        self.obj2 = Summarizer(Summary = Sum)

        self.obj1._results.update({
            (1, ): Sum(contents = np.array((4, ))),
            (2, ): Sum(contents = np.array((3, ))),
            (3, ): Sum(contents = np.array((2, ))),
            })

        self.obj2._results.update({
            (2, ): Sum(contents = np.array((3.2, ))),
            (4, ): Sum(contents = np.array((2, ))),
        })

        self.expected = {
            (1, ): Sum(contents = np.array((4, ))),
            (2, ): Sum(contents = np.array((6.2, ))),
            (3, ): Sum(contents = np.array((2, ))),
            (4, ): Sum(contents = np.array((2, ))),
            }

    def test_add(self):
        obj3 = self.obj1 + self.obj2
        self.assertEqual(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results[(1, )], obj3._results[(1, )])
        self.assertIsNot(self.obj2._results[(4, )], obj3._results[(4, )])

    def test_radd(self):
        obj3 = sum([self.obj1, self.obj2]) # 0 + obj1 is executed
        self.assertEqual(self.expected, obj3._results)
        self.assertIsNot(self.obj1._results[(1, )], obj3._results[(1, )])
        self.assertIsNot(self.obj2._results[(4, )], obj3._results[(4, )])

    def test_iadd(self):
        obj1 = self.obj1

        self.obj1 += self.obj2
        self.assertIs(self.obj1, obj1)
        self.assertEqual(self.expected, self.obj1._results)

    def test_copy(self):
        copy1 = copy.copy(self.obj1)
        self.assertEqual(self.obj1._results, copy1._results)
        self.assertIsNot(self.obj1._results[(1, )], copy1._results[(1, )])
        self.assertIsNot(self.obj1._results[(2, )], copy1._results[(2, )])
        self.assertIsNot(self.obj1._results[(3, )], copy1._results[(3, )])

##__________________________________________________________________||
