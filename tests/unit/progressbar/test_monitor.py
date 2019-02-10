# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.progressbar import BProgressMonitor, NullProgressMonitor, ProgressMonitor

##__________________________________________________________________||
def build_BProgressMonitor():
    return BProgressMonitor(presentation=None)

def build_ProgressMonitor():
    return ProgressMonitor(presentation=None)

def build_NullProgressMonitor():
    return NullProgressMonitor()

builds = [build_BProgressMonitor, build_ProgressMonitor, build_NullProgressMonitor]
build_ids = ['BProgressMonitor', 'ProgressMonitor', 'NullProgressMonitor']

##__________________________________________________________________||
@pytest.mark.parametrize('build', builds, ids=build_ids)
def test_monitor(build):
    obj = build()
    obj.begin()
    obj.createReporter()
    obj.end()

##__________________________________________________________________||
