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
        max_files_per_run = 2

        expected = [
            (['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 30),
            (['B'], 20, 20)
        ]
        self.assertEqual(expected, create_file_start_length_list(file_nevents_list, max_events_per_run, max_events_total, max_files_per_run))

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

    def test_file_start_length_list_empty_01(self):
        args = ([ ], 20, 2) # empty file list
        expected = [ ]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 0)], 20, 2) # no events
        expected = [ ]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 0), ('B', 0), ('C', 0)], 20, 2) # no events
        expected = [ ]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 0), ('B', 10), ('C', 0)], 20, 2) # no events in some files
        expected = [(['B'], 0, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 0), ('B', 20), ('C', 0)], 20, 2) # the last file has no events
                                                        # the 2nd last has max_events_per_run
        expected = [(['B'], 0, 20)] # shouldn't be [(['B'], 0, 20), ([ ], 0, 0)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20), ('B', 0), ('C', 0)], 20, 2)
        expected = [(['A'], 0, 20)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_onefile_01(self):
        args = ([('A', 20)], 30, 2)
        expected = [(['A'], 0, 20)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20)], 20, 2)
        expected = [(['A'], 0, 20)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20)], 10, 2)
        expected = [(['A'], 0, 10), (['A'], 10, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20)], 7, 2)
        expected = [(['A'], 0, 7), (['A'], 7, 7), (['A'], 14, 6)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_twofiles_01(self):

        args = ([('A', 20), ('B', 20)], 20, 2) # exact
        expected = [(['A'], 0, 20), (['B'], 0, 20)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20), ('B', 25)], 20, 2) # exact first file
        expected = [(['A'], 0, 20), (['B'], 0, 20), (['B'], 20, 5)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 40), ('B', 25)], 20, 2) # twice the exact first file
        expected = [(['A'], 0, 20), (['A'], 20, 20), (['B'], 0, 20), (['B'], 20, 5)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 60), ('B', 25)], 20, 2) # three times the exact first file
        expected = [(['A'], 0, 20), (['A'], 20, 20), (['A'], 40, 20), (['B'], 0, 20), (['B'], 20, 5)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 20)], 110, 2) # short first file
        expected = [(['A', 'B'], 0, 110), (['B'], 10, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20), ('B', 25)], 30, 2) # short first file
        expected = [(['A', 'B'], 0, 30), (['B'], 10, 15)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20), ('B', 100)], 30, 2) # short first file
        expected = [(['A', 'B'], 0, 30), (['B'], 10, 30), (['B'], 40, 30), (['B'], 70, 30)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 30)], 30, 2) # long first file
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 30), (['B'], 20, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_twofiles_02_maxfile1(self):

        args = ([('A', 20), ('B', 20)], 20, 1) # exact
        expected = [(['A'], 0, 20), (['B'], 0, 20)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20), ('B', 25)], 20, 1) # exact fist file
        expected = [(['A'], 0, 20), (['B'], 0, 20), (['B'], 20, 5)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 20)], 110, 1) # short first file
        expected = [(['A'], 0, 100), (['B'], 0, 20)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20), ('B', 25)], 30, 1) # short first file
        expected = [(['A'], 0, 20), (['B'], 0, 25)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 20), ('B', 100)], 30, 1) # short first file
        expected = [(['A'], 0, 20), (['B'], 0, 30), (['B'], 30, 30), (['B'], 60, 30), (['B'], 90, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 30)], 30, 1) # long first file
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A'], 90, 10), (['B'], 0, 30)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 90), ('B', 30)], 30, 1) # long first file
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['B'], 0, 30)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_03(self):
        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 30)], 30, 10)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 22)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_04(self):
        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 10)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 30), (['D'], 38, 30), (['D'], 68, 30), (['D'], 98, 2)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 3)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C'], 90, 22), (['D'], 0, 30), (['D'], 30, 30), (['D'], 60, 30), (['D'], 90, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('C', 7), ('D', 100)], 30, 2)
        expected = [(['C', 'D'], 0, 30), (['D'], 23, 30), (['D'], 53, 30), (['D'], 83, 17)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 2)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 15), (['C', 'D'], 0, 30), (['D'], 23, 30), (['D'], 53, 30), (['D'], 83, 17)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 1)
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A'], 90, 10), (['B'], 0, 5), (['C'], 0, 7), (['D'], 0, 30), (['D'], 30, 30), (['D'], 60, 30), (['D'], 90, 10)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_05(self):

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, -1) # max_files_per_run = -1
        expected = [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 30), (['D'], 38, 30), (['D'], 68, 30), (['D'], 98, 2)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], -1, 2) # max_events_per_run = -1
        expected = [(['A', 'B'], 0, 105), (['C', 'D'], 0, 107)]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], -1, -1) # both are -1
        expected = [(['A', 'B', 'C', 'D'], 0, 212)]
        self.assertEqual(expected, _file_start_length_list(*args))

    def test_file_start_length_list_06(self):

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 0) # max_files_per_run = 0
        expected = [ ]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 0, 2) # max_events_per_run = 0
        expected = [ ]
        self.assertEqual(expected, _file_start_length_list(*args))

        args = ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 0, 0) # both are 0
        expected = [ ]
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
