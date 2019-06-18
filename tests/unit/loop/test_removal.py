# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from alphatwirl.loop import EventsInDatasetReader

##__________________________________________________________________||
removed_classes = [EventsInDatasetReader]

@pytest.mark.parametrize('Class', removed_classes)
def test_removed(Class, caplog):
    with pytest.raises(RuntimeError):
       with caplog.at_level(logging.ERROR):
          c = Class()
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    expected = '{} is removed.'.format(Class.__name__)
    assert expected in caplog.records[0].msg

##__________________________________________________________________||

