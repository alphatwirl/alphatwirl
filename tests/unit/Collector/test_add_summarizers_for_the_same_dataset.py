import unittest
import itertools

from AlphaTwirl.Collector.functions import add_summarizers_for_the_same_dataset

##__________________________________________________________________||
class MockSummarizer(object):
    def __init__(self):
        self._content = [id(self)]

    def __add__(self, other):
        ret = MockSummarizer()
        ret._content[:] =  list(itertools.chain(*[self._content, other._content]))
        return ret

    def __eq__(self, other):
        return sorted(self._content) == sorted(other._content)

    def __ne__(self, other):
        return not self.__eq__(other)

##__________________________________________________________________||
class TestMockSummarizer(unittest.TestCase):

    def test_one_reader(self):

        obj1 = MockSummarizer()
        obj2 = MockSummarizer()
        obj3 = MockSummarizer()

        self.assertEqual(obj1, obj1)
        self.assertEqual(obj2, obj2)
        self.assertEqual(obj3, obj3)

        self.assertNotEqual(obj1, obj2)
        self.assertNotEqual(obj1, obj3)
        self.assertNotEqual(obj2, obj3)

        self.assertEqual(obj1 + obj2, obj1 + obj2)
        self.assertEqual(obj1 + obj2, obj2 + obj1) # independent of the order

        self.assertEqual(obj1 + obj2 + obj3, obj1 + obj2 + obj3)

        self.assertNotEqual(obj1 + obj2, obj1)
        self.assertNotEqual(obj1 + obj2, obj1 + obj3)

##__________________________________________________________________||
class Test_add_summarizers_for_the_same_dataset(unittest.TestCase):

    def test_empty(self):

        dataset_summarizer_pairs = [ ]

        expected = [ ]

        actual = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        self.assertEqual(expected, actual)

    def test_false_empty_list(self):

        dataset_summarizer_pairs = [
            ('data1',  [ ]) # empty list
        ]

        expected = [ ]

        actual = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        self.assertEqual(expected, actual)

    def test_false_None(self):

        dataset_summarizer_pairs = [
            ('data1',  None) #
        ]

        expected = [ ]

        actual = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        self.assertEqual(expected, actual)

    def test_one_pair(self):

        summarizer = MockSummarizer()

        dataset_summarizer_pairs = [
            ('data1', summarizer)
        ]

        expected  = [
            ('data1', summarizer)
        ]

        actual = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        self.assertEqual(expected, actual)

    def test_two_pairs(self):

        summarizer1 = MockSummarizer()
        summarizer2 = MockSummarizer()

        dataset_summarizer_pairs = [
            ('data1', summarizer1),
            ('data2', summarizer2),

        ]

        expected  = [
            ('data1', summarizer1),
            ('data2', summarizer2)
            ]

        actual = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        self.assertEqual(expected, actual)

    def test_the_same_dataset(self):

        summarizer1 = MockSummarizer()
        summarizer2 = MockSummarizer()
        summarizer3 = MockSummarizer()

        dataset_summarizer_pairs = [
            ('data1', summarizer1),
            ('data2', summarizer2),
            ('data1', summarizer3),

        ]

        expected  = [
            ('data1', summarizer1 + summarizer3),
            ('data2', summarizer2),
        ]

        actual = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        self.assertEqual(expected, actual)

    def test_the_order(self):

        summarizer1 = MockSummarizer()
        summarizer2 = MockSummarizer()
        summarizer3 = MockSummarizer()

        dataset_summarizer_pairs = [
            ('data2', summarizer1),
            ('data1', summarizer2),
            ('data2', summarizer3),
        ]

        expected  = [
            ('data2', summarizer1 + summarizer3),
            ('data1', summarizer2),
        ]

        actual = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        self.assertEqual(expected, actual)

##__________________________________________________________________||
