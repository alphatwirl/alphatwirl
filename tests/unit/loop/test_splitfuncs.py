# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop.splitfuncs import create_files_start_length_list
from alphatwirl.loop.splitfuncs import _file_nevents_list
from alphatwirl.loop.splitfuncs import _fast_path
from alphatwirl.loop.splitfuncs import _need_get_number_of_events_in_files

##__________________________________________________________________||
@pytest.fixture()
def mock_fast_path(monkeypatch):
    module = sys.modules['alphatwirl.loop.splitfuncs']
    ret = mock.Mock(name='mock_fast_path')
    monkeypatch.setattr(module, '_fast_path', ret)
    return ret

@pytest.fixture()
def mock_full_path(monkeypatch):
    module = sys.modules['alphatwirl.loop.splitfuncs']
    ret = mock.Mock(name='mock_full_path')
    monkeypatch.setattr(module, '_full_path', ret)
    return ret

@pytest.mark.parametrize('files', [[], ['A.root'], ['A.root', 'B.root', 'C.root']])
@pytest.mark.parametrize('max_events', [-1, 0, 1, 100])
@pytest.mark.parametrize('max_events_per_run', [-1, 0, 1, 100])
@pytest.mark.parametrize('max_files', [-1, 0, 1, 100])
@pytest.mark.parametrize('max_files_per_run', [-1, 0, 1, 100])
def test_create_files_start_length_list(
        files, max_events, max_events_per_run,
        max_files, max_files_per_run,
        mock_fast_path, mock_full_path
):
    actual = create_files_start_length_list(
        files,
        func_get_nevents_in_file=None,
        max_events=max_events,
        max_events_per_run=max_events_per_run,
        max_files=max_files,
        max_files_per_run=max_files_per_run
    )

##__________________________________________________________________||
def test_create_files_start_length_list_default():
    files = mock.sentinel.files
    actual = create_files_start_length_list(files)
    assert [(files, 0, -1)] == actual

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
@pytest.mark.parametrize('files, max_files_per_run, expected', [
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], -1,
        [(['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 0, -1)]
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 0,
        [ ]
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 1,
        [
            (['A.root'], 0, -1),
            (['B.root'], 0, -1),
            (['C.root'], 0, -1),
            (['D.root'], 0, -1),
            (['E.root'], 0, -1)
        ]
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 2,
        [
            (['A.root', 'B.root'], 0, -1),
            (['C.root', 'D.root'], 0, -1),
            (['E.root'], 0, -1)
        ]
    ),
])
def test_fast_path(files, max_files_per_run, expected):
    actual = _fast_path(files, max_files_per_run)
    assert expected == actual

##__________________________________________________________________||
@pytest.mark.parametrize('max_events, max_events_per_run, expected', [
    ( 0,  0,  True),
    ( 0, -1,  True),
    ( 0,  1,  True),
    (-1,  0,  True),
    (-1, -1, False),
    (-1,  1, True),
    ( 1,  0, True),
    ( 1, -1 , True),
    ( 1,  1, True),
])
def test_need_get_number_of_events_in_files(max_events, max_events_per_run, expected):
    actual = _need_get_number_of_events_in_files(max_events, max_events_per_run)
    assert expected == actual

##__________________________________________________________________||

