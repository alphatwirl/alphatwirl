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
