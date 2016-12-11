import unittest
import collections
import numpy as np

from AlphaTwirl.Collector import combinedToList, CombineIntoList

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, results):
        self._results = results

    def results(self):
        return self._results

##__________________________________________________________________||
class MockResult(object):
    def __init__(self, results):
        self._results = results

    def results(self):
        return self._results

##__________________________________________________________________||
MockCount = collections.namedtuple('MockCount', 'contents')

##__________________________________________________________________||
class TestCombinedToList(unittest.TestCase):

    def test_combine_oneReader(self):

        results = MockResult(
            {
                (1, ): MockCount(contents = [np.array((4, 6))]),
                (2, ): MockCount(contents = [np.array((3, 9))]),
                (3, ): MockCount(contents = [np.array((2, 3))]),
            }
        )

        combined = [
            ('data1', results)
        ]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
            ('data1', 1, 4, 6),
            ('data1', 2, 3, 9),
            ('data1', 3, 2, 3),
        ]

        columns = ('component', 'v1', 'n', 'nvar')

        self.assertEqual(expected, combinedToList(combined, columns))

    def test_combine_twoReaders(self):

        results1 = MockResult(
            {
                (1, ): MockCount(contents = [np.array((4, 6))]),
                (2, ): MockCount(contents = [np.array((3, 9))]),
                (3, ): MockCount(contents = [np.array((2, 3))]),
            }
        )

        results2 = MockResult(
            {
                (2, ): MockCount(contents = [np.array((3, 6))]),
                (4, ): MockCount(contents = [np.array((2, 2))]),
            }
        )

        combined = [
            ('data1', results1),
            ('data2', results2),
        ]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
            ('data1', 1, 4, 6),
            ('data1', 2, 3, 9),
            ('data1', 3, 2, 3),
            ('data2', 2, 3, 6),
            ('data2', 4, 2, 2),
        ]

        columns = ('component', 'v1', 'n', 'nvar')

        self.assertEqual(expected, combinedToList(combined, columns))

    def test_combine_with_empty_counts(self):

        results1 = MockResult(
            {
                (1, ): MockCount(contents = [np.array((4, 6))]),
                (2, ): MockCount(contents = [np.array((3, 9))]),
                (3, ): MockCount(contents = [np.array((2, 3))]),
            }
        )

        results2 = MockResult({})

        combined = [
            ('data1', results1),
            ('data2', results2),
        ]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
            ('data1', 1, 4, 6),
            ('data1', 2, 3, 9),
            ('data1', 3, 2, 3),
        ]

        columns = ('component', 'v1', 'n', 'nvar')

        self.assertEqual(expected, combinedToList(combined, columns))

    def test_combine_all_empty_counts(self):

        results1 = MockResult({})

        results2 = MockResult({})

        combined = [
            ('data1', results1),
            ('data2', results2),
        ]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
        ]

        columns = ('component', 'v1', 'n', 'nvar')

        self.assertEqual(expected, combinedToList(combined, columns))

    def test_combine_empty_pairs(self):

        combined = [ ]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
        ]

        columns = ('component', 'v1', 'n', 'nvar')

        self.assertEqual(expected, combinedToList(combined, columns))

##__________________________________________________________________||
class TestCombineIntoList(unittest.TestCase):

    def test_combine_oneReader(self):

        reader = MockReader(
            MockResult(
                {
                    (1, ): MockCount(contents = [np.array((4, 6))]),
                    (2, ): MockCount(contents = [np.array((3, 9))]),
                    (3, ): MockCount(contents = [np.array((2, 3))]),
                }
            )
        )
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

        reader1 = MockReader(
            MockResult(
                {
                    (1, ): MockCount(contents = [np.array((4, 6))]),
                    (2, ): MockCount(contents = [np.array((3, 9))]),
                    (3, ): MockCount(contents = [np.array((2, 3))]),
                }
            )
        )

        reader2 = MockReader(
            MockResult(
                {
                    (2, ): MockCount(contents = [np.array((3, 6))]),
                    (4, ): MockCount(contents = [np.array((2, 2))]),
                }
            )
        )

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

        reader1 = MockReader(
            MockResult(
                {
                    (1, ): MockCount(contents = [np.array((4, 6))]),
                    (2, ): MockCount(contents = [np.array((3, 9))]),
                    (3, ): MockCount(contents = [np.array((2, 3))]),
                }
            )
        )

        reader2 = MockReader(MockResult({}))

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

        reader1 = MockReader(MockResult({}))

        reader2 = MockReader(MockResult({}))

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
