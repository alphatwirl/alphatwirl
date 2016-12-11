import unittest
import collections
import numpy as np

from AlphaTwirl.Collector import CombineIntoList

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, summarizer):
        self.summarizer = summarizer

    def results(self):
        return self.summarizer

##__________________________________________________________________||
class MockSummarizer(object):
    def __init__(self, results):
        self._results = results

    def results(self):
        return self._results

##__________________________________________________________________||
MockSummary = collections.namedtuple('MockSummary', 'contents')

##__________________________________________________________________||
class TestCombineIntoList(unittest.TestCase):

    def test_combine_oneReader(self):

        reader = MockReader(
            MockSummarizer(
                {
                    (1, ): MockSummary(contents = [np.array((4, 6))]),
                    (2, ): MockSummary(contents = [np.array((3, 9))]),
                    (3, ): MockSummary(contents = [np.array((2, 3))]),
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
            MockSummarizer(
                {
                    (1, ): MockSummary(contents = [np.array((4, 6))]),
                    (2, ): MockSummary(contents = [np.array((3, 9))]),
                    (3, ): MockSummary(contents = [np.array((2, 3))]),
                }
            )
        )

        reader2 = MockReader(
            MockSummarizer(
                {
                    (2, ): MockSummary(contents = [np.array((3, 6))]),
                    (4, ): MockSummary(contents = [np.array((2, 2))]),
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
            MockSummarizer(
                {
                    (1, ): MockSummary(contents = [np.array((4, 6))]),
                    (2, ): MockSummary(contents = [np.array((3, 9))]),
                    (3, ): MockSummary(contents = [np.array((2, 3))]),
                }
            )
        )

        reader2 = MockReader(MockSummarizer({}))

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

        reader1 = MockReader(MockSummarizer({}))

        reader2 = MockReader(MockSummarizer({}))

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
