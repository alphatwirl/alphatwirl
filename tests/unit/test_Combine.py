import unittest
import itertools

from AlphaTwirl import Combine

##__________________________________________________________________||
class MockResult(object):
    def __init__(self):
        self._content = [id(self)]

    def __add__(self, other):
        ret = MockResult()
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
class TestMockResult(unittest.TestCase):

    def test_one_reader(self):

        obj1 = MockResult()
        obj2 = MockResult()
        obj3 = MockResult()

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

        result = MockResult()
        reader = MockReader(result)
        datasetReaderPairs = [('data1', reader), ]

        expected  = {
            'data1': result
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_two_readers(self):

        result1 = MockResult()
        reader1 = MockReader(result1)

        result2 = MockResult()
        reader2 = MockReader(result2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected  = {
            'data1': result1,
            'data2': result2
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_two_readers_the_same_dataset(self):

        result1 = MockResult()
        reader1 = MockReader(result1)

        result2 = MockResult()
        reader2 = MockReader(result2)

        datasetReaderPairs = [('data1', reader1), ('data1', reader2)]

        expected  = {
            'data1': result1 + result2,
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_empty_pairs(self):

        datasetReaderPairs = [ ]

        expected = { }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

##__________________________________________________________________||
