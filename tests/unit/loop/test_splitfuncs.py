import sys
import unittest

from alphatwirl.loop.splitfuncs import *
from alphatwirl.loop.splitfuncs import _apply_max_events_total
from alphatwirl.loop.splitfuncs import _file_start_length_list
from alphatwirl.loop.splitfuncs import _start_length_pairs_for_split_lists
from alphatwirl.loop.splitfuncs import _minimum_positive_value

##__________________________________________________________________||
class TestSplitfuncs(unittest.TestCase):

    def test_create_file_start_length_list(self):

        # simple
        file_nevents_list = [('A', 100), ('B', 100)]
        max_events_per_run = 30
        max_events_total = 140

        expected = [
            ('A', 0, 30), ('A', 30, 30), ('A', 60, 30), ('A', 90, 10),
            ('B', 0, 30), ('B', 30, 10),
        ]
        self.assertEqual(expected, create_file_start_length_list(file_nevents_list, max_events_per_run, max_events_total))

        # no split
        file_nevents_list = [('A', 100), ('B', 100)]
        max_events_per_run = -1
        max_events_total = 140
        expected = [('A', 0, 100), ('B', 0, 40)]
        self.assertEqual(expected, create_file_start_length_list(file_nevents_list, max_events_per_run, max_events_total))

        # no split, no max
        file_nevents_list = [('A', 100), ('B', 100)]
        max_events_per_run = -1
        max_events_total = -1
        expected = [('A', 0, 100), ('B', 0, 100)]
        self.assertEqual(expected, create_file_start_length_list(file_nevents_list, max_events_per_run, max_events_total))

    def test_apply_max_events_total(self):

        # simple
        file_nevents_list = [('A', 100), ('B', 100)]
        max_events_total = 120
        expected = [('A', 100), ('B', 20)]
        self.assertEqual(expected, _apply_max_events_total(file_nevents_list, max_events_total))

        # exact
        file_nevents_list = [('A', 100), ('B', 200)]
        max_events_total = 300
        expected = [('A', 100), ('B', 200)]
        self.assertEqual(expected, _apply_max_events_total(file_nevents_list, max_events_total))

        # default
        file_nevents_list = [('A', 100), ('B', 200)]
        expected = [('A', 100), ('B', 200)]
        self.assertEqual(expected, _apply_max_events_total(file_nevents_list))

        # zero
        file_nevents_list = [('A', 100), ('B', 200)]
        max_events_total = 0
        expected = [ ]
        self.assertEqual(expected, _apply_max_events_total(file_nevents_list, max_events_total))

        # empty
        file_nevents_list = [ ]
        max_events_total = 10
        expected = [ ]
        self.assertEqual(expected, _apply_max_events_total(file_nevents_list, max_events_total))

    def test_file_start_length_list_01(self):
        args = ([('A', 100), ('B', 20)], 110, 2)
        expected = [(['A', 'B'], 0, 110), (['B'], 10, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_02(self):
        args = ([('A', 100), ('B', 30)], 30, 2)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 30), (['B'], 20, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_03(self):
        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 30)], 30, 10)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 22)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_04(self):
        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 10)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 30), (['D'], 38, 30), (['D'], 68, 30), (['D'], 98, 2)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_05(self):
        args = ([('A', 20), ('B', 25)], 30, 2)
        expected = [(['A', 'B'], 0, 30), (['B'], 10, 15)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_06(self):
        args = ([('A', 20), ('B', 100)], 30, 2)
        expected = [(['A', 'B'], 0, 30), (['B'], 10, 30), (['B'], 40, 30), (['B'], 70, 30)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_07(self):
        args = ([('A', 20), ('B', 25)], 20, 2)
        expected = [(['A'], 0, 20), (['B'], 0, 20), (['B'], 20, 5)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_start_length_pairs_for_split_lists(self):
        self.assertEqual([(0, 10), (10, 10), (20, 10), (30, 10)], _start_length_pairs_for_split_lists(40, 10))
        self.assertEqual([(0, 10), (10, 10), (20, 10), (30, 10), (40, 1)], _start_length_pairs_for_split_lists(41, 10))
        self.assertEqual([(0, 40)], _start_length_pairs_for_split_lists(40, 40))
        self.assertEqual([(0, 40)], _start_length_pairs_for_split_lists(40, 50))

        self.assertEqual([(0, 40)], _start_length_pairs_for_split_lists(40, -1))

    def test_minimum_positive_value(self):

        # empty
        self.assertEqual(-1, _minimum_positive_value([]))

        # all negative
        self.assertEqual(-1, _minimum_positive_value([-1, -2, - 3]))

        # all positive
        self.assertEqual(10, _minimum_positive_value([10, 20, 30]))

        # zero or positive
        self.assertEqual(0, _minimum_positive_value([10, 20, 0, 30]))

        # general
        self.assertEqual(10, _minimum_positive_value([10, 20, 30, -2, -3]))

##__________________________________________________________________||
