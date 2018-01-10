# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import BProgressMonitor, ProgressReporter

##__________________________________________________________________||
@pytest.fixture()
def presentation():
    return mock.MagicMock()

@pytest.fixture()
def monitor(presentation):
    return BProgressMonitor(presentation)


##__________________________________________________________________||
def test_repr(monitor):
    repr(monitor)

def test_begin_end(monitor):
    monitor.begin()
    monitor.end()

def test_createReporter(monitor):
    assert isinstance(monitor.createReporter(), ProgressReporter)

##__________________________________________________________________||
