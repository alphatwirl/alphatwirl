# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import os
import errno
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl import mkdir_p

##__________________________________________________________________||
@pytest.fixture()
def mock_makedirs(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(os, 'makedirs', ret)
    return ret

@pytest.fixture()
def mock_isdir(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(os.path, 'isdir', ret)
    return ret

##__________________________________________________________________||
def test_emtpy(mock_makedirs):
    mkdir_p('')
    assert [ ] == mock_makedirs.call_args_list

def test_success(mock_makedirs):
    mkdir_p('a/b')
    assert [mock.call('a/b')] == mock_makedirs.call_args_list

def test_already_exist(mock_makedirs, mock_isdir, caplog):
    mock_isdir.return_value = True
    mock_makedirs.side_effect = OSError(errno.EEXIST, 'already exist')
    with caplog.at_level(logging.DEBUG - 1):
        mkdir_p('a/b')

    assert [mock.call('a/b')] == mock_makedirs.call_args_list
    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.DEBUG - 1
    assert 'tried' in caplog.records[0].msg

def test_raise(mock_makedirs, mock_isdir, caplog):
    mock_isdir.return_value = False
    mock_makedirs.side_effect = OSError
    with pytest.raises(OSError):
        mkdir_p('a/b')

    assert [mock.call('a/b')] == mock_makedirs.call_args_list

##__________________________________________________________________||
