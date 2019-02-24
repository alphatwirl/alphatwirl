# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from alphatwirl.progressbar import BProgressMonitor, NullProgressMonitor, ProgressMonitor
from alphatwirl.progressbar.presentation import Presentation

##__________________________________________________________________||
class MockProgressBar(Presentation):
    def _present(self):
        pass

##__________________________________________________________________||
def build_BProgressMonitor():
    return BProgressMonitor(presentation=MockProgressBar())

def build_ProgressMonitor():
    return ProgressMonitor(presentation=MockProgressBar)

def build_NullProgressMonitor():
    return NullProgressMonitor()

builds = [build_BProgressMonitor, build_ProgressMonitor, build_NullProgressMonitor]
build_ids = ['BProgressMonitor', 'ProgressMonitor', 'NullProgressMonitor']

##__________________________________________________________________||
@pytest.mark.parametrize('build', builds, ids=build_ids)
def test_monitor(build):
    obj = build()
    obj.begin()
    obj.create_reporter()
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('build', builds, ids=build_ids)
def test_deprecated(build, caplog):
    with caplog.at_level(logging.WARNING):
        obj = build()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'progressbar' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

##__________________________________________________________________||
