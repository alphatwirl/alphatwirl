# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import DatasetIntoEventBuildersSplitter

##__________________________________________________________________||
@pytest.fixture()
def MockEventBuilder():
    return mock.Mock()

@pytest.fixture()
def mockConfigMaker():
    ret = mock.Mock()
    file_list = ['A.root', 'B.root', 'C.root', 'D.root', 'E.root']
    def file_list_in(dataset, maxFiles):
        if maxFiles < 0:
            return file_list
        else:
            return file_list[:maxFiles]
    ret.file_list_in.side_effect = file_list_in
    ret.nevents_in_file.side_effect = [100, 200, 150, 180, 210]
    return ret

@pytest.fixture()
def obj(MockEventBuilder, mockConfigMaker):
    ret = DatasetIntoEventBuildersSplitter(
        EventBuilder=MockEventBuilder,
        eventBuilderConfigMaker=mockConfigMaker
    )
    return ret

def test_repr(obj):
   repr(obj)

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
def test_need_get_number_of_events_in_files(obj, max_events, max_events_per_run, expected):
    actual = obj._need_get_number_of_events_in_files(max_events, max_events_per_run)
    assert expected == actual

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
def test_fast_path(obj, files, max_files_per_run, expected):
    actual = obj._fast_path(files, max_files_per_run)
    assert expected == actual

@pytest.mark.parametrize('files, max_events, max_events_per_run, max_files_per_run, expected', [
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'],
        330, 80, 2,
        [
            (['A.root'], 0, 80), (['A.root', 'B.root'], 80, 80),
            (['B.root'], 60, 80), (['B.root', 'C.root'], 140, 80),
            (['C.root'], 20, 10)
        ]
    ),
])
def test_full_path(obj, files, max_events, max_events_per_run, max_files_per_run, expected):
    actual = obj._full_path(files, max_events, max_events_per_run, max_files_per_run)
    assert expected == actual

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
        obj, files, nevents, max_events,
        expected_results, expected_call_args):
    func_get_nevents_in_file = mock.Mock()
    func_get_nevents_in_file.side_effect = nevents
    actual = obj._file_nevents_list_(
        files,
        func_get_nevents_in_file=func_get_nevents_in_file,
        max_events=max_events
    )
    assert expected_results == actual
    assert [mock.call(a) for a in expected_call_args] == func_get_nevents_in_file.call_args_list

def test_create_configs(obj, mockConfigMaker):
    dataset = mock.Mock()
    file_start_length_list = [('A.root', 0, 40), ('A.root', 40, 40), ('B.root', 0, 10)]
    config1 = mock.Mock()
    config2 = mock.Mock()
    config3 = mock.Mock()
    mockConfigMaker.create_config_for.side_effect = [config1, config2, config3]
    actual = obj._create_configs(dataset, file_start_length_list)
    assert [config1, config2, config3] == actual
    assert [
        mock.call(dataset, 'A.root', 0, 40),
        mock.call(dataset, 'A.root', 40, 40),
        mock.call(dataset, 'B.root', 0, 10),
    ] == mockConfigMaker.create_config_for.call_args_list

def test_call(obj):
    dataset = mock.Mock()
    obj(dataset)

##__________________________________________________________________||
