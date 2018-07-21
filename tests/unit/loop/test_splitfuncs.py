# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop.splitfuncs import create_files_start_length_list
from alphatwirl.loop.splitfuncs import _apply_max_files
from alphatwirl.loop.splitfuncs import _file_nevents_list
from alphatwirl.loop.splitfuncs import _fast_path

##__________________________________________________________________||
@pytest.fixture()
def wrapped_apply_max_files(monkeypatch):
    module = sys.modules['alphatwirl.loop.splitfuncs']
    ret = mock.Mock(wraps=_apply_max_files)
    monkeypatch.setattr(module, '_apply_max_files', ret)
    return ret

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
        wrapped_apply_max_files,
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

    wrapped_apply_max_files.assert_called_once()

    if max_events == 0 or max_events_per_run == 0:
        assert [ ] == actual
    elif max_events < 0 and max_events_per_run < 0:
        assert mock_fast_path() == actual
    else:
        assert mock_full_path() == actual

##__________________________________________________________________||
def test_create_files_start_length_list_default():
    file1 = mock.sentinel.file1
    file2 = mock.sentinel.file2
    file3 = mock.sentinel.file3
    files = [file1, file2, file3]
    actual = create_files_start_length_list(files)
    assert [([file1], 0, -1), ([file2], 0, -1), ([file3], 0, -1)] == actual

##__________________________________________________________________||
@pytest.mark.parametrize('args, expected', [

    ## empty
    pytest.param(([ ], -1), [ ], id='empty. -1'),
    pytest.param(([ ],  0), [ ], id='empty. 0'),
    pytest.param(([ ],  1), [ ], id='empty. 1'),
    pytest.param(([ ], 10), [ ], id='empty. 10'),
    pytest.param((['A.root' ], -1), ['A.root'], id='1 file. -1'),
    pytest.param((['A.root' ],  0), [ ], id='1 file. 0'),
    pytest.param((['A.root' ],  1), ['A.root'], id='1 file. 1'),
    pytest.param((['A.root' ], 10), ['A.root'], id='1 file. 10'),
    pytest.param(
        (
            ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
            -1
        ),
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='all'
    ),
    pytest.param(
        (['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 0),
        [ ],
        id='zero'
    ),
    pytest.param(
        (['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 1),
        ['A.root'],
        id='one'
    ),
    pytest.param(
        (['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 3),
        ['A.root', 'B.root', 'C.root'],
        id='smaller max_events'
    ),
    pytest.param(
        (['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 5),
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='exact max_events'
    ),
    pytest.param(
        (['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 10),
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='larger max_events'
    ),
])
def test_apply_max_files(args, expected):
    assert expected == _apply_max_files(*args)

##__________________________________________________________________||
@pytest.mark.parametrize(
    'files, nevents, max_events, expected_results, expected_call_args', [
    pytest.param([ ], [ ], -1, [ ], [ ], id='empty-no-max'),
    pytest.param([ ], [ ], 10, [ ], [ ], id='empty-with-max'),
    pytest.param(
        ['A.root'], [100], -1, [('A.root', 100)],
        ['A.root'],
        id='one-file-no-max'
    ),
    pytest.param(
        ['A.root'], [100], 0, [ ],
        [ ],
        id='one-file-zero-max'
    ),
    pytest.param(
        ['A.root'], [0], -1, [ ],
        ['A.root'],
        id='one-file-empty'
    ),
    pytest.param(
        ['A.root'], [None], -1, [ ],
        ['A.root'],
        id='one-file-error'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        -1,
        [('A.root', 100), ('B.root', 200), ('C.root', 150), ('D.root', 180), ('E.root', 210)],
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='five-files-no-max'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        0,
        [ ],
        [ ],
        id='five-files-zero-max'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        150,
        [('A.root', 100), ('B.root', 200)],
        ['A.root', 'B.root'],
        id='five-files-with-max'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 200, 150, 180, 210],
        300, # exactly the nevents in the first two files
        [('A.root', 100), ('B.root', 200)],
        ['A.root', 'B.root'],
        id='five-files-max-exactly-first-two-files'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, 0, 150, 180, 210],
        -1,
        [('A.root', 100), ('C.root', 150), ('D.root', 180), ('E.root', 210)],
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='five-files-one-empty-file'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [0, 0, 0, 0, 0],
        -1,
        [ ],
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='five-files-all-empty'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [100, None, 150, 180, 210],
        -1,
        [('A.root', 100), ('C.root', 150), ('D.root', 180), ('E.root', 210)],
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='five-files-one-error-file'
    ),
    pytest.param(
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        [None, None, None, None, None],
        -1,
        [ ],
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        id='five-files-all-error'
    ),
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
