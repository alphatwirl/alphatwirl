import sys
import unittest

from AlphaTwirl.Loop.splitfuncs import *
from AlphaTwirl.Loop.splitfuncs import _apply_max_total
from AlphaTwirl.Loop.splitfuncs import _start_length_pairs_for_split_lists
from AlphaTwirl.Loop.splitfuncs import _minimum_positive_value

##__________________________________________________________________||
class TestSplitfuncs(unittest.TestCase):

    def test_create_file_start_length_list(self):

        # simple
        file_nevents_list = [('A', 100), ('B', 100)]
        max_per_run = 30
        max_total = 140

        expected = [
            ('A', 0, 30), ('A', 30, 30), ('A', 60, 30), ('A', 90, 10),
            ('B', 0, 30), ('B', 30, 10),
        ]
        self.assertEqual(expected, create_file_start_length_list(file_nevents_list, max_per_run, max_total))

        # no split
        file_nevents_list = [('A', 100), ('B', 100)]
        max_per_run = -1
        max_total = 140
        expected = [('A', 0, 100), ('B', 0, 40)]
        self.assertEqual(expected, create_file_start_length_list(file_nevents_list, max_per_run, max_total))

        # no split, no max
        file_nevents_list = [('A', 100), ('B', 100)]
        max_per_run = -1
        max_total = -1
        expected = [('A', 0, 100), ('B', 0, 100)]
        self.assertEqual(expected, create_file_start_length_list(file_nevents_list, max_per_run, max_total))

    def test_apply_max_total(self):

        # simple
        file_nevents_list = [('A', 100), ('B', 100)]
        max_total = 120
        expected = [('A', 100), ('B', 20)]
        self.assertEqual(expected, _apply_max_total(file_nevents_list, max_total))

        # exact
        file_nevents_list = [('A', 100), ('B', 200)]
        max_total = 300
        expected = [('A', 100), ('B', 200)]
        self.assertEqual(expected, _apply_max_total(file_nevents_list, max_total))

        # default
        file_nevents_list = [('A', 100), ('B', 200)]
        expected = [('A', 100), ('B', 200)]
        self.assertEqual(expected, _apply_max_total(file_nevents_list))

        # zero
        file_nevents_list = [('A', 100), ('B', 200)]
        max_total = 0
        expected = [ ]
        self.assertEqual(expected, _apply_max_total(file_nevents_list, max_total))

        # empty
        file_nevents_list = [ ]
        max_total = 10
        expected = [ ]
        self.assertEqual(expected, _apply_max_total(file_nevents_list, max_total))

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
