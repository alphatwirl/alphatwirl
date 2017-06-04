import unittest
import collections
import numpy as np

from alphatwirl.collector import ToTupleList

from .mock import MockReader, MockSummarizer

##__________________________________________________________________||
class TestToTupleList(unittest.TestCase):

    def setUp(self):
        self.obj = ToTupleList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar')
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
            ('htbin', 'njetbin', 'n', 'nvar'),
            (200, 2, 120, 240),
            (300, 2, 490, 980),
            (300, 3, 210, 420),
            (300, 2, 20, 40),
            (300, 3, 15, 30)
        ]

        actual = self.obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

    def test_combine_oneReader(self):

        obj = ToTupleList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar')
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
            ('htbin', 'njetbin', 'n', 'nvar'),
            (200, 2, 120, 240),
            (300, 2, 310, 620),
        ]

        actual = obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

    def test_combine_all_empty_contents(self):

        obj = ToTupleList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar')
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
            ('htbin', 'njetbin', 'n', 'nvar'),
        ]

        actual = obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

    def test_combine_empty_pairs(self):

        obj = ToTupleList(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar')
        )

        dataset_readers_list = [ ]

        expected = None

        actual = obj.combine(dataset_readers_list)

        self.assertEqual(expected, actual)

##__________________________________________________________________||
