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
def mock_split_func():
    ret = mock.Mock()
    ret.return_value = [
        (['A.root'], 0, 80), (['A.root', 'B.root'], 80, 80),
        (['B.root'], 60, 80), (['B.root', 'C.root'], 140, 80),
        (['C.root'], 20, 10)
    ]
    return ret

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
def obj(MockEventBuilder, mockConfigMaker, mock_split_func):
    ret = DatasetIntoEventBuildersSplitter(
        EventBuilder=MockEventBuilder,
        eventBuilderConfigMaker=mockConfigMaker
    )
    ret.create_file_start_length_list = mock_split_func
    return ret

def test_repr(obj):
   repr(obj)

def test_file_start_length_list_fast_path_00(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = -1        # < 0
    maxEventsPerRun = -1  # < 0
    maxFiles = -1         # < 0
    maxFilesPerRun = -1
    expected = [
        (['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 0, -1),
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=-1)] == mockConfigMaker.file_list_in.call_args_list
    assert [ ] == mock_split_func.call_args_list

def test_file_start_length_list_fast_path_01(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = -1        # < 0
    maxEventsPerRun = -1  # < 0
    maxFiles = -1         # < 0
    maxFilesPerRun = 1
    expected = [
        (['A.root'], 0, -1),
        (['B.root'], 0, -1),
        (['C.root'], 0, -1),
        (['D.root'], 0, -1),
        (['E.root'], 0, -1)
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=-1)] == mockConfigMaker.file_list_in.call_args_list
    assert [ ] == mock_split_func.call_args_list

def test_file_start_length_list_fast_path_02(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = -1        # < 0
    maxEventsPerRun = -1  # < 0
    maxFiles = -1         # < 0
    maxFilesPerRun = 2    # > 0
    expected = [
        (['A.root', 'B.root'], 0, -1),
        (['C.root', 'D.root'], 0, -1),
        (['E.root'], 0, -1)
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=-1)] == mockConfigMaker.file_list_in.call_args_list
    assert [ ] == mock_split_func.call_args_list

def test_file_start_length_list_fast_path_03(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = -1        # < 0
    maxEventsPerRun = -1  # < 0
    maxFiles = 3          # > 0
    maxFilesPerRun = 2    # > 0
    expected = [
        (['A.root', 'B.root'], 0, -1),
        (['C.root'], 0, -1),
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=3)] == mockConfigMaker.file_list_in.call_args_list
    assert [ ] == mock_split_func.call_args_list

def test_file_start_length_list_fast_path_04(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = -1        # < 0
    maxEventsPerRun = -1  # < 0
    maxFiles = 0          # = 0
    maxFilesPerRun = 2    # > 0
    expected = [
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=0)] == mockConfigMaker.file_list_in.call_args_list
    assert [ ] == mock_split_func.call_args_list

def test_file_start_length_list_fast_path_05(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = -1        # < 0
    maxEventsPerRun = -1  # < 0
    maxFiles = 0          # = 0
    maxFilesPerRun = 0    # = 0
    expected = [
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=0)] == mockConfigMaker.file_list_in.call_args_list
    assert [ ] == mock_split_func.call_args_list

def test_file_start_length_list_fast_path_06(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = -1        # < 0
    maxEventsPerRun = -1  # < 0
    maxFiles = -1         # < 0
    maxFilesPerRun = 0    # = 0
    expected = [
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=-1)] == mockConfigMaker.file_list_in.call_args_list
    assert [ ] == mock_split_func.call_args_list

def test_file_start_length_list_long_path(obj, mockConfigMaker, mock_split_func):
    dataset = mock.Mock()
    maxEvents = 330        # > 0
    maxEventsPerRun = 80   # > 0
    maxFiles = 4           # > 0
    maxFilesPerRun = 2     # > 0
    expected = [
        (['A.root'], 0, 80), (['A.root', 'B.root'], 80, 80),
        (['B.root'], 60, 80), (['B.root', 'C.root'], 140, 80),
        (['C.root'], 20, 10)
    ]
    actual = obj._file_start_length_list(
        dataset, maxEvents=maxEvents, maxEventsPerRun=maxEventsPerRun,
        maxFiles=maxFiles, maxFilesPerRun=maxFilesPerRun
    )
    assert expected == actual
    assert [mock.call(dataset, maxFiles=4)] == mockConfigMaker.file_list_in.call_args_list
    assert [mock.call(
        file_nevents_list=[('A.root', 100), ('B.root', 200), ('C.root', 150)],
        max_events_per_run=80, max_events_total=330, max_files_per_run=2
    )] == mock_split_func.call_args_list

@pytest.mark.parametrize('files, maxFilesPerRun, expected', [
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
def test_fast_path(obj, files, maxFilesPerRun, expected):
    actual = obj._fast_path(files, maxFilesPerRun)
    assert expected == actual

@pytest.mark.parametrize('files, maxEvents, expected', [
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], -1,
        [('A.root', 100), ('B.root', 200), ('C.root', 150), ('D.root', 180), ('E.root', 210)]
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 0,
        [ ]
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 150,
        [('A.root', 100), ('B.root', 200)]
    ),
    (
        ['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 300,
        [('A.root', 100), ('B.root', 200)]
    ),
])
def test_file_nevents_list_(obj, files, maxEvents, expected):
    actual = obj._file_nevents_list_(files, maxEvents=maxEvents)
    assert expected == actual

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
