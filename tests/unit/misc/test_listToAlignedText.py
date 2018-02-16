# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from alphatwirl import listToAlignedText

##__________________________________________________________________||
def test_deprecated(caplog):
    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        listToAlignedText('')

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'listToAlignedText' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

def test_name():
    assert  'listToAlignedText' == listToAlignedText.__name__

##__________________________________________________________________||
