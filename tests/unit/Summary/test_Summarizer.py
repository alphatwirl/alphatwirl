import unittest
import copy

from AlphaTwirl.Summary import Summarizer

##__________________________________________________________________||
class MockSummary(object):
    def __init__(self, val = None, weight = 1, contents = None):

        if contents is not None:
            self.contents = contents
            return

        if val is None:
            self.contents = 0
            return

        self.contents = val*weight

    def __add__(self, other):
        contents = self.contents + other.contents
        return self.__class__(contents = contents)

    def __radd__(self, other):
        # is called with other = 0 when e.g. sum([obj1, obj2])
        return self.__class__() + self

    def __repr__(self):
        return '{}(contents = {})'.format(self.__class__.__name__, self.contents)

    def __eq__(self, other):
        return self.contents == other.contents

##__________________________________________________________________||
class MockSummary2(object):
    def __init__(self, val = None, weight = 1, contents = None):
        pass

##__________________________________________________________________||
class TestMockSummary(unittest.TestCase):

    def test_01(self):
        obj0 = MockSummary()
        obj1 = MockSummary(val = 11)
        self.assertIsNot(obj1, sum([obj1])) # will call __radd__(other = 0)
        obj2 = MockSummary(val = 22)
        obj3 = MockSummary(val = 33)
        self.assertEqual(obj3, (obj1 + obj2))
        obj4 = MockSummary(val = 43)
        self.assertNotEqual(obj4, (obj1 + obj2))

##__________________________________________________________________||
class TestSummarizer(unittest.TestCase):

    def test_init_repr(self):
        obj = Summarizer(Summary = MockSummary)
        repr(obj)

    def test_add(self):

        obj = Summarizer(Summary = MockSummary)

        obj.add('A', 12)
        expected  = {'A': MockSummary(contents = 12)}
        self.assertEqual(expected, obj.results())

        obj.add('A', 23)
        expected  = {'A': MockSummary(contents = 35)}
        self.assertEqual(expected, obj.results())

        obj.add('A', 10, weight = 2)
        expected  = {'A': MockSummary(contents = 55)}
        self.assertEqual(expected, obj.results())

        obj.add('B', 20, weight = 3.2)
        expected  = {
            'A': MockSummary(contents = 55),
            'B': MockSummary(contents = 64.0)
        }
        self.assertEqual(expected, obj.results())

        return

    def test_add_key(self):
        obj = Summarizer(Summary = MockSummary)
        obj.add_key('A')
        expected  = {'A': MockSummary(contents = 0)}
        self.assertEqual(expected, obj.results())

        obj.add_key('B')
        obj.add_key('C')
        expected  = {
            'A': MockSummary(contents = 0),
            'B': MockSummary(contents = 0),
            'C': MockSummary(contents = 0),
        }
        self.assertEqual(expected, obj.results())

    def test_copy_from(self):
        obj = Summarizer(Summary = MockSummary2)
        src_obj = Summarizer(Summary = MockSummary)

        src_results  = {
            'A': MockSummary(contents = 55),
            'B': MockSummary(contents = 64.0)
        }

        src_obj._results.update(src_results)
        obj.copy_from(src_obj)
        self.assertEqual(src_results, obj.results())
        self.assertIsNot(src_obj._results, obj._results)
        self.assertEqual(obj.Summary, src_obj.Summary)
        self.assertIsNot(src_obj._results['A'], obj._results['A'])
        self.assertIsNot(src_obj._results['B'], obj._results['B'])

##__________________________________________________________________||
class TestSummarizer_operator(unittest.TestCase):

    def setUp(self):
        self.obj1 = Summarizer(Summary = MockSummary)
        self.obj2 = Summarizer(Summary = MockSummary)

        self.obj1._results  = {
            (1, ): MockSummary(contents = 4),
            (2, ): MockSummary(contents = 3),
            (3, ): MockSummary(contents = 2),
            }

        self.obj2._results  = {
            (2, ): MockSummary(contents = 3.2),
            (4, ): MockSummary(contents = 2),
        }

        self.expected = {
            (1, ): MockSummary(contents = 4),
            (2, ): MockSummary(contents = 6.2),
            (3, ): MockSummary(contents = 2),
            (4, ): MockSummary(contents = 2),
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


##__________________________________________________________________||
