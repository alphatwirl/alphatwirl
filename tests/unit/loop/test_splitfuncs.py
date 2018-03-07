# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import DatasetIntoEventBuildersSplitter

from alphatwirl.loop.splitfuncs import _file_nevents_list
from alphatwirl.loop.splitfuncs import create_file_start_length_list

##__________________________________________________________________||
@pytest.mark.parametrize(
    'files, nevents, max_events, expected_results, expected_call_args', [
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        -1,
        [('A.root', 100), ('B.root', 200), ('C.root', 150), ('D.root', 180), ('E.root', 210)],
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        0,
        [ ],
        [ ],
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        150,
        [('A.root', 100), ('B.root', 200)],
        ['A.root', 'B.root'],
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        300, # exactly the nevents in the first two files
        [('A.root', 100), ('B.root', 200)],
        ['A.root', 'B.root'],
    ),
    ([ ], [ ], -1, [ ], [ ]),
    ([ ], [ ], 10, [ ], [ ]),
])
def test_file_nevents_list_(
        files, nevents, max_events,
        expected_results, expected_call_args):
    func_get_nevents_in_file = mock.Mock()
    func_get_nevents_in_file.side_effect = nevents
    actual = _file_nevents_list(
        files,
        func_get_nevents_in_file=func_get_nevents_in_file,
        max_events=max_events
    )
    assert expected_results == actual
    assert [mock.call(a) for a in expected_call_args] == func_get_nevents_in_file.call_args_list

##__________________________________________________________________||
def test_create_file_start_length_list():

    # simple
    file_nevents_list = [('A', 100), ('B', 100)]
    max_events_per_run = 30
    max_events_total = 140
    max_files_per_run = 2

    expected = [
        (['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 30),
        (['B'], 20, 20)
    ]
    assert expected == create_file_start_length_list(file_nevents_list, max_events_per_run, max_events_total, max_files_per_run)

##__________________________________________________________________||
