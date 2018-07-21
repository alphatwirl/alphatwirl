# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop.splitfuncs import create_files_start_length_list
from alphatwirl.loop.splitfuncs import _full_path
from alphatwirl.loop.splitfuncs import _files_start_length_list

##__________________________________________________________________||
# 'args, expected'
params = [
    ## empty
    pytest.param(([ ], 20, 2), [ ], id='empty-file-list'),
    pytest.param(([('A', 0)], 20, 2), [ ], id='no-events-one-file'),
    pytest.param(([('A', 0), ('B', 0), ('C', 0)], 20, 2), [ ], id='no-events-multiple-files'),
    pytest.param(([('A', 0), ('B', 10), ('C', 0)], 20, 2), [(['B'], 0, 10)], id='no-events-in-some-files'),
    pytest.param(
        ([('A', 0), ('B', 20), ('C', 0)], 20, 2), # the last file has no events.
                                                  # the 2nd last has max_events_per_run.
        [(['B'], 0, 20)], # shouldn't be [(['B'], 0, 20), ([ ], 0, 0)]
        id='empty-after-max'
    ),
    pytest.param(([('A', 20), ('B', 0), ('C', 0)], 20, 2), [(['A'], 0, 20)], id='max-empty-empty'),

    ## one file
    pytest.param(([('A', 20)], 30, 2), [(['A'], 0, 20)], id='one-file'),
    pytest.param(([('A', 20)], 20, 2), [(['A'], 0, 20)], id='one-file-2'),
    pytest.param(([('A', 20)], 10, 2), [(['A'], 0, 10), (['A'], 10, 10)], id='one-file-3'),
    pytest.param(([('A', 20)], 7, 2), [(['A'], 0, 7), (['A'], 7, 7), (['A'], 14, 6)], id='one-file-4'),

    ## two files
    pytest.param(
        ([('A', 20), ('B', 20)], 20, 2),
        [(['A'], 0, 20), (['B'], 0, 20)],
        id='two-files-exact'
    ),
    pytest.param(
        ([('A', 20), ('B', 25)], 20, 2),
        [(['A'], 0, 20), (['B'], 0, 20), (['B'], 20, 5)],
        id='two-files-exact-first-file'
    ),
    pytest.param(
        ([('A', 40), ('B', 25)], 20, 2),
        [(['A'], 0, 20), (['A'], 20, 20), (['B'], 0, 20), (['B'], 20, 5)],
        id='two-files-twice-the-exact-first-file'
    ),
    pytest.param(
        ([('A', 60), ('B', 25)], 20, 2),
        [(['A'], 0, 20), (['A'], 20, 20), (['A'], 40, 20), (['B'], 0, 20), (['B'], 20, 5)],
        id='two-files-three-times-the-exact-first-file'
    ),
    pytest.param(
        ([('A', 100), ('B', 20)], 110, 2),
        [(['A', 'B'], 0, 110), (['B'], 10, 10)],
        id='two-files-short-first-file'
    ),
    pytest.param(
        ([('A', 20), ('B', 25)], 30, 2),
        [(['A', 'B'], 0, 30), (['B'], 10, 15)],
        id='two-files-short-first-file-2'
    ),
    pytest.param(
        ([('A', 20), ('B', 100)], 30, 2),
        [(['A', 'B'], 0, 30), (['B'], 10, 30), (['B'], 40, 30), (['B'], 70, 30)],
        id='two-files-short-first-file-3'
    ),
    pytest.param(
        ([('A', 100), ('B', 30)], 30, 2),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 30), (['B'], 20, 10)],
        id='two-files-long-first-file'
    ),

    ## two files, max_files_per_run=1
    pytest.param(
        ([('A', 20), ('B', 20)], 20, 1),
        [(['A'], 0, 20), (['B'], 0, 20)],
        id='two-files-maxfile1-exact'
    ),
    pytest.param(
        ([('A', 20), ('B', 25)], 20, 1),
        [(['A'], 0, 20), (['B'], 0, 20), (['B'], 20, 5)],
        id='two-files-maxfile1-exact-fist-file'
    ),
    pytest.param(
        ([('A', 100), ('B', 20)], 110, 1),
        [(['A'], 0, 100), (['B'], 0, 20)],
        id='two-files-maxfile1-short-first-file'
    ),
    pytest.param(
        ([('A', 20), ('B', 25)], 30, 1),
        [(['A'], 0, 20), (['B'], 0, 25)],
        id='two-files-maxfile1-short-first-file-2'
    ),
    pytest.param(
        ([('A', 20), ('B', 100)], 30, 1),
        [(['A'], 0, 20), (['B'], 0, 30), (['B'], 30, 30), (['B'], 60, 30), (['B'], 90, 10)],
        id='two-files-maxfile1-short-first-file-3'
    ),
    pytest.param(
        ([('A', 100), ('B', 30)], 30, 1),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A'], 90, 10), (['B'], 0, 30)],
        id='two-files-maxfile1-long-first-file'
    ),
    pytest.param(
        ([('A', 90), ('B', 30)], 30, 1),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['B'], 0, 30)],
        id='two-files-maxfile1-long-first-file-2'
    ),

    ##
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 30)], 30, 10),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 22)],
        id='four-flies'
    ),

    ##
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 10),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 30), (['D'], 38, 30), (['D'], 68, 30), (['D'], 98, 2)],
        id='four-files-one-run-with-all-files'
    ),
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 3),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C'], 90, 22), (['D'], 0, 30), (['D'], 30, 30), (['D'], 60, 30), (['D'], 90, 10)],
        id='four-files-maxfile-3'
    ),
    pytest.param(
        ([('C', 7), ('D', 100)], 30, 2),
        [(['C', 'D'], 0, 30), (['D'], 23, 30), (['D'], 53, 30), (['D'], 83, 17)],
        id='two-files-first-run-with-two-files'
    ),
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 2),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 15), (['C', 'D'], 0, 30), (['D'], 23, 30), (['D'], 53, 30), (['D'], 83, 17)],
        id='four-files-max-file-2'
    ),
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 1),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A'], 90, 10), (['B'], 0, 5), (['C'], 0, 7), (['D'], 0, 30), (['D'], 30, 30), (['D'], 60, 30), (['D'], 90, 10)],
        id='four-files-max-file-1'
    ),

    ## -1
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, -1),
        [(['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B', 'C', 'D'], 90, 30), (['D'], 8, 30), (['D'], 38, 30), (['D'], 68, 30), (['D'], 98, 2)],
        id='no-max_files_per_run'
    ),
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], -1, 2),
        [(['A', 'B'], 0, 105), (['C', 'D'], 0, 107)],
        id='no-max_events_per_run'
    ),
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], -1, -1),
        [(['A', 'B', 'C', 'D'], 0, 212)],
        id='no-max_events_per_run-no-max_files_per_run'
    ),

    ## 0
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 30, 0),
        [ ],
        id='zero-max_files_per_run'
    ),
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 0, 2),
        [ ],
        id='zero-max_events_per_run'
    ),
    pytest.param(
        ([('A', 100), ('B', 5), ('C', 7), ('D', 100)], 0, 0),
        [ ],
        id='zero-max_events_per_run-zero-max_files_per_run'
    ),
]

##__________________________________________________________________||
@pytest.mark.parametrize('args, expected', params)
def test_files_start_length_list(args, expected):
    assert expected == _files_start_length_list(*args)

@pytest.mark.parametrize('args, expected', params)
def test_create_files_start_length_list(args, expected):
    file_nevents_list = args[0]
    files, nevents = zip(*file_nevents_list) if file_nevents_list else (( ), ( ))
    max_events_per_run = args[1]
    max_files_per_run = args[2]
    func_get_nevents_in_file = mock.Mock()
    func_get_nevents_in_file.side_effect = nevents

    if not max_events_per_run >= 0:
        # _files_start_length_list() won't be called
        return

    assert expected == create_files_start_length_list(
        files=files,
        func_get_nevents_in_file=func_get_nevents_in_file,
        max_events=-1,
        max_events_per_run=max_events_per_run,
        max_files=-1,
        max_files_per_run=max_files_per_run
    )

@pytest.mark.parametrize('args, expected', params)
def test_full_path(args, expected):
    file_nevents_list = args[0]
    files, nevents = zip(*file_nevents_list) if file_nevents_list else (( ), ( ))
    max_events_per_run = args[1]
    max_files_per_run = args[2]
    func_get_nevents_in_file = mock.Mock()
    func_get_nevents_in_file.side_effect = nevents

    assert expected == _full_path(
        files=files,
        func_get_nevents_in_file=func_get_nevents_in_file,
        max_events=-1,
        max_events_per_run=max_events_per_run,
        max_files_per_run=max_files_per_run
    )
##__________________________________________________________________||
