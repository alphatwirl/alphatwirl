# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from alphatwirl.roottree import EventBuilder, BEventBuilder

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
if has_no_ROOT:
    removed_classes = [ ]
else:
    removed_classes = [EventBuilder, BEventBuilder]

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

