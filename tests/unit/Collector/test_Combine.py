import unittest
import itertools

from AlphaTwirl.Collector import Combine

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
class MockReader(object):
    def __init__(self, results = None):
        self._results = results

    def results(self):
        return self._results

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
class TestCombine(unittest.TestCase):

    def assert_np_dict_frame(self, f1, f2):
        self.assertEqual(sorted(f1.keys()), sorted(f2.keys()))
        for k in sorted(f1.keys()):
            np.testing.assert_equal(f1[k], f2[k])

    def test_one_reader(self):

        summarizer = MockSummarizer()
        reader = MockReader(summarizer)
        datasetReaderPairs = [('data1', reader), ]

        expected  = {
            'data1': summarizer
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_two_readers(self):

        summarizer1 = MockSummarizer()
        reader1 = MockReader(summarizer1)

        summarizer2 = MockSummarizer()
        reader2 = MockReader(summarizer2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected  = {
            'data1': summarizer1,
            'data2': summarizer2
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_two_readers_the_same_dataset(self):

        summarizer1 = MockSummarizer()
        reader1 = MockReader(summarizer1)

        summarizer2 = MockSummarizer()
        reader2 = MockReader(summarizer2)

        datasetReaderPairs = [('data1', reader1), ('data1', reader2)]

        expected  = {
            'data1': summarizer1 + summarizer2,
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_empty_pairs(self):

        datasetReaderPairs = [ ]

        expected = { }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

##__________________________________________________________________||
