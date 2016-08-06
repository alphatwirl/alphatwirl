import unittest
import numpy as np
import collections

from AlphaTwirl import Combine

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, results): self._results = results
    def results(self): return self._results

##__________________________________________________________________||
class TestCombine(unittest.TestCase):

    def assert_np_dict_frame(self, f1, f2):
        self.assertEqual(sorted(f1.keys()), sorted(f2.keys()))
        for k in sorted(f1.keys()):
            np.testing.assert_equal(f1[k], f2[k])

    def test_one_reader(self):

        counts  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)),
            (3, ): np.array((2, 3)),
            }

        reader = MockReader(counts)
        datasetReaderPairs = [('data1', reader), ]

        expected  = {
            ('data1', 1): np.array((4, 6)),
            ('data1', 2): np.array((3, 9)),
            ('data1', 3): np.array((2, 3)),
            }

        combine = Combine()
        self.assert_np_dict_frame(expected, combine.combine(datasetReaderPairs))

    def test_two_readers(self):

        counts1  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)),
            (3, ): np.array((2, 3)),
        }

        reader1 = MockReader(counts1)

        counts2  = {
            (2, ): np.array((3, 6)),
            (4, ): np.array((2, 2)),
        }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected  = {
            ('data1', 1): np.array((4, 6)),
            ('data1', 2): np.array((3, 9)),
            ('data1', 3): np.array((2, 3)),
            ('data2', 2): np.array((3, 6)),
            ('data2', 4): np.array((2, 2)),
        }

        combine = Combine()
        self.assert_np_dict_frame(expected, combine.combine(datasetReaderPairs))

    def test_two_readers_the_same_dataset(self):

        counts1  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)),
            (3, ): np.array((2, 3)),
        }

        reader1 = MockReader(counts1)

        counts2  = {
            (2, ): np.array((3, 6)),
            (4, ): np.array((2, 2)),
        }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data1', reader2)]

        expected  = {
            ('data1', 1): np.array((4,  6)),
            ('data1', 2): np.array((6, 15)),
            ('data1', 3): np.array((2,  3)),
            ('data1', 4): np.array((2,  2)),
        }

        combine = Combine()
        self.assert_np_dict_frame(expected, combine.combine(datasetReaderPairs))

    def test_two_readers_not_same_object(self):

        counts1  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)),
            (3, ): np.array((2, 3)),
        }

        reader1 = MockReader(counts1)

        counts2  = {
            (2, ): np.array((3, 6)),
            (4, ): np.array((2, 2)),
        }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected  = {
            ('data1', 1): np.array((4, 6)),
            ('data1', 2): np.array((3, 9)),
            ('data1', 3): np.array((2, 3)),
            ('data2', 2): np.array((3, 6)),
            ('data2', 4): np.array((2, 2)),
        }

        combine = Combine()
        actual = combine.combine(datasetReaderPairs)
        self.assert_np_dict_frame(expected, actual)
        self.assertIsNot(counts1[(1, )], actual[('data1', 1)])

    def test_combine_with_empty_counts(self):

        counts1  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)),
            (3, ): np.array((2, 3)),
            }

        reader1 = MockReader(counts1)

        counts2  = { }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected  = {
            ('data1', 1): np.array((4, 6)),
            ('data1', 2): np.array((3, 9)),
            ('data1', 3): np.array((2, 3)),
            }

        combine = Combine()
        self.assert_np_dict_frame(expected, combine.combine(datasetReaderPairs))

    def test_combine_all_empty_counts(self):

        counts1  = { }

        reader1 = MockReader(counts1)

        counts2  = { }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = { }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_empty_pairs(self):

        datasetReaderPairs = [ ]

        expected = { }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

##__________________________________________________________________||
