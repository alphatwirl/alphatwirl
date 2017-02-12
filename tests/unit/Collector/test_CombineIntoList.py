import unittest
import collections
import copy
import numpy as np

from AlphaTwirl.Collector import CombineIntoList

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

    def results(self):
        return self._results

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self._results
        )

    def __add__(self, other):
        res = copy.deepcopy(self._results)
        for k, v in other._results.iteritems():
            if k not in res:
                res[k] = copy.deepcopy(v)
            else:
                res[k].contents[0] = res[k].contents[0] + v.contents[0]
        return self.__class__(res)

##__________________________________________________________________||
MockSummary = collections.namedtuple('MockSummary', 'contents')

##__________________________________________________________________||
class TestCombineIntoList(unittest.TestCase):

    def test_repr(self):
        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            sort = True,
            datasetColumnName = 'dataset'
        )
        repr(obj)

    def test_example(self):

        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            sort = True,
            datasetColumnName = 'dataset'
        )

        reader1 = MockReader(
            MockSummarizer(
                collections.OrderedDict([
                    ((200, 2), MockSummary(contents = [np.array((120, 240))])),
                    ((300, 2), MockSummary(contents = [np.array((310, 620))])),
                ])
            )
        )

        reader2 = MockReader(
            MockSummarizer(
                collections.OrderedDict([
                    ((300, 2), MockSummary(contents = [np.array((180, 360))])),
                    ((300, 3), MockSummary(contents = [np.array((210, 420))])),
                ])
            )
        )

        reader3 = MockReader(
            MockSummarizer(
                collections.OrderedDict([
                    ((300, 2), MockSummary(contents = [np.array((20, 40))])),
                    ((300, 3), MockSummary(contents = [np.array((15, 30))])),
                ])
            )
        )

        reader4 = MockReader(
            MockSummarizer(
                collections.OrderedDict([])
            )
        )

        datasetReaderPairs = [
            ('QCD', reader1),
            ('QCD', reader2),
            ('TTJets', reader3),
            ('WJets', reader4),
        ]

        expected = [
            ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
            ('QCD', 200, 2, 120, 240),
            ('QCD', 300, 2, 490, 980),
            ('QCD', 300, 3, 210, 420),
            ('TTJets', 300, 2, 20, 40),
            ('TTJets', 300, 3, 15, 30)
        ]

        actual = obj.combine(datasetReaderPairs)

        self.assertEqual(expected, actual)

    def test_combine_oneReader(self):

        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            sort = True,
            datasetColumnName = 'dataset'
        )

        reader1 = MockReader(
            MockSummarizer(
                collections.OrderedDict([
                    ((200, 2), MockSummary(contents = [np.array((120, 240))])),
                    ((300, 2), MockSummary(contents = [np.array((310, 620))])),
                ])
            )
        )

        datasetReaderPairs = [
            ('QCD', reader1),
        ]

        expected = [
            ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
            ('QCD', 200, 2, 120, 240),
            ('QCD', 300, 2, 310, 620),
        ]

        actual = obj.combine(datasetReaderPairs)

        self.assertEqual(expected, actual)

    def test_combine_all_empty_contents(self):

        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            sort = True,
            datasetColumnName = 'dataset'
        )

        reader1 = MockReader(
            MockSummarizer(
                collections.OrderedDict([])
            )
        )

        reader2 = MockReader(
            MockSummarizer(
                collections.OrderedDict([])
            )
        )
        reader3 = MockReader(
            MockSummarizer(
                collections.OrderedDict([])
            )
        )

        datasetReaderPairs = [
            ('QCD', reader1),
            ('QCD', reader2),
            ('TTJets', reader3),
        ]

        expected = [
            ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
        ]

        actual = obj.combine(datasetReaderPairs)

        self.assertEqual(expected, actual)

    def test_combine_empty_pairs(self):

        obj = CombineIntoList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            sort = True,
            datasetColumnName = 'dataset'
        )

        datasetReaderPairs = [ ]

        expected = None

        actual = obj.combine(datasetReaderPairs)

        self.assertEqual(expected, actual)

##__________________________________________________________________||
