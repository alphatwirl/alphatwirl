from AlphaTwirl import countsToList, CombineIntoList
import unittest
import numpy as np

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, results):
        self._results = results

    def valNames(self):
        return ('n', 'nvar')

    def results(self):
        return self._results

##__________________________________________________________________||
class TestCountsToList(unittest.TestCase):

    def test_call(self):

        counts  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)),
            (3, ): np.array((2, 3)),
        }

        expected = [
            ('v1', 'n', 'nvar'),
            (1, 4, 6),
            (2, 3, 9),
            (3, 2, 3),
        ]

        columns = ('v1', 'n', 'nvar')
        self.assertEqual(expected, countsToList(counts, columns))

    def test_call_threeValues(self):

        counts  = {
            (1, ): np.array((4, 6, 2.3)),
            (2, ): np.array((3, 9, 5.4)),
            (3, ): np.array((2, 3, 3.6)),
            }

        expected = [
            ('v1', 'n', 'nvar', 'skewness'),
            (1, 4.0, 6.0, 2.3),
            (2, 3.0, 9.0, 5.4),
            (3, 2.0, 3.0, 3.6)
        ]

        columns = ('v1', 'n', 'nvar', 'skewness')
        self.assertEqual(expected, countsToList(counts, columns))

##__________________________________________________________________||
class TestCombineIntoList(unittest.TestCase):

    def test_combine_oneReader(self):

        counts  = {
            (1, ): np.array((4, 6)),
            (2, ): np.array((3, 9)),
            (3, ): np.array((2, 3)),
            }

        reader = MockReader(counts)
        datasetReaderPairs = [('data1', reader), ]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
            ('data1', 1, 4, 6),
            ('data1', 2, 3, 9),
            ('data1', 3, 2, 3),
        ]

        combine = CombineIntoList(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_twoReaders(self):

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

        expected = [
            ('component', 'v1', 'n', 'nvar'),
            ('data1', 1, 4, 6),
            ('data1', 2, 3, 9),
            ('data1', 3, 2, 3),
            ('data2', 2, 3, 6),
            ('data2', 4, 2, 2),
        ]

        combine = CombineIntoList(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

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

        expected = [
            ('component', 'v1', 'n', 'nvar'),
            ('data1', 1, 4, 6),
            ('data1', 2, 3, 9),
            ('data1', 3, 2, 3),
        ]

        combine = CombineIntoList(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_all_empty_counts(self):

        counts1  = { }

        reader1 = MockReader(counts1)

        counts2  = { }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
        ]

        combine = CombineIntoList(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_empty_pairs(self):

        datasetReaderPairs = [ ]

        combine = CombineIntoList(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(None, combine.combine(datasetReaderPairs))

##__________________________________________________________________||
