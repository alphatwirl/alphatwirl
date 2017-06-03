import unittest
import collections
import copy
import numpy as np

from alphatwirl.collector import CombineIntoList

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, summarizer):
        self.summarizer = summarizer

    def results(self):
        return self.summarizer

    def __repr__(self):
        return '{}(summarizer = {!r})'.format(
            self.__class__.__name__,
            self.summarizer
        )

##__________________________________________________________________||
class MockSummarizer(object):
    def __init__(self, results):
        self._results = results

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self._results
        )

    def __add__(self, other):
        if other == 0:
            res = copy.copy(self._results)
        else:
            res = copy.copy(self._results) + copy.copy(other._results)
        return self.__class__(res)

    def __radd__(self, other):
        return self.__add__(other)

    def to_tuple_list(self):
        return self._results

##__________________________________________________________________||
class TestCombineIntoList(unittest.TestCase):

    def setUp(self):
        self.obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            datasetColumnName = 'dataset'
        )

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_example(self):

        reader1 = MockReader(
            MockSummarizer(
                [
                    (200, 2, 120, 240),
                ]))

        reader2 = MockReader(
            MockSummarizer(
                [
                    (300, 2, 490, 980),
                    (300, 3, 210, 420),
                ]))

        reader3 = MockReader(
            MockSummarizer(
                [
                    (300, 2, 20, 40),
                    (300, 3, 15, 30),
                ]))

        reader4 = MockReader(MockSummarizer([]))

        dataset_readers_list = [
            ('QCD', (reader1, reader2)),
            ('TTJets', (reader3, )),
            ('WJets', (reader4, )),
            ('ZJets', ( )),
        ]

        expected = [
            ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
            ('QCD', 200, 2, 120, 240),
            ('QCD', 300, 2, 490, 980),
            ('QCD', 300, 3, 210, 420),
            ('TTJets', 300, 2, 20, 40),
            ('TTJets', 300, 3, 15, 30)
        ]

        actual = self.obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

    def test_combine_oneReader(self):

        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            datasetColumnName = 'dataset'
        )

        reader1 = MockReader(
            MockSummarizer(
                [
                    (200, 2, 120, 240),
                    (300, 2, 310, 620),
                ]))

        dataset_readers_list = [
            ('QCD', (reader1, )),
        ]

        expected = [
            ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
            ('QCD', 200, 2, 120, 240),
            ('QCD', 300, 2, 310, 620),
        ]

        actual = obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

    def test_combine_all_empty_contents(self):

        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            datasetColumnName = 'dataset'
        )

        reader1 = MockReader(
            MockSummarizer(
                [ ]))

        reader2 = MockReader(
            MockSummarizer(
                [ ]))

        reader3 = MockReader(
            MockSummarizer(
                [ ]))

        dataset_readers_list = [
            ('QCD', (reader1, reader2)),
            ('TTJets', (reader3, )),
        ]

        expected = [
            ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
        ]

        actual = obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

    def test_combine_empty_pairs(self):

        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            datasetColumnName = 'dataset'
        )

        dataset_readers_list = [ ]

        expected = None

        actual = obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

##__________________________________________________________________||
