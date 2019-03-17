# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from alphatwirl.concurrently.exec_util import try_executing_until_succeed, exec_command, compose_shortened_command_for_logging

##__________________________________________________________________||
def test_try_executing_until_succeed(caplog):
    with caplog.at_level(logging.WARNING):
        try_executing_until_succeed(['ls'])
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'alphatwirl.concurrently.exec_util' in caplog.records[0].name
    assert 'is deprecated' in caplog.records[0].msg

def test_exec_command(caplog):
    with caplog.at_level(logging.WARNING):
        exec_command(['ls'])
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'alphatwirl.concurrently.exec_util' in caplog.records[0].name
    assert 'is deprecated' in caplog.records[0].msg

def test_compose_shortened_command_for_logging(caplog):
    with caplog.at_level(logging.WARNING):
        compose_shortened_command_for_logging(['ls'])
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'alphatwirl.concurrently.exec_util' in caplog.records[0].name
    assert 'is deprecated' in caplog.records[0].msg

##__________________________________________________________________||

