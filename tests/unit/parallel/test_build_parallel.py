# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.parallel import build_parallel
from alphatwirl.parallel.build import build_parallel_multiprocessing

##__________________________________________________________________||
@pytest.fixture(
    params=[True, False]
)
def isatty(request, monkeypatch):
    ret = request.param
    org_stdout = sys.stdout
    f = mock.Mock(**{
        'stdout.isatty.return_value': ret,
        'stdout.write.side_effect': lambda x : org_stdout.write(x)
    })
    module = sys.modules['alphatwirl.parallel.build']
    monkeypatch.setattr(module, 'sys', f)
    return ret

##__________________________________________________________________||
@pytest.mark.parametrize('processes', [0, 1, 3])
@pytest.mark.parametrize('quiet', [True, False])
def test_build_parallel_multiprocessing(quiet, processes, isatty):

    parallel_mode = 'multiprocessing'
    parallel = build_parallel(
        parallel_mode=parallel_mode,
        quiet=quiet,
        processes=processes,
    )

    ## progressMonitor
    if quiet:
        assert 'NullProgressMonitor' == parallel.progressMonitor.__class__.__name__
    elif processes == 0:
        assert 'ProgressMonitor' == parallel.progressMonitor.__class__.__name__
    else:
        assert 'BProgressMonitor' == parallel.progressMonitor.__class__.__name__

    if not quiet:
        if isatty:
            assert 'ProgressBar' == parallel.progressMonitor.presentation.__class__.__name__
        else:
            assert 'ProgressPrint' == parallel.progressMonitor.presentation.__class__.__name__

    ## communicationChannel
    if processes == 0:
        assert 'CommunicationChannel0' == parallel.communicationChannel.__class__.__name__
    else:
        assert 'CommunicationChannel' == parallel.communicationChannel.__class__.__name__
        assert 'MultiprocessingDropbox' ==  parallel.communicationChannel.dropbox.__class__.__name__

    ## workingarea
    assert parallel.workingarea is None

##__________________________________________________________________||
def test_build_logging_unknown_parallel_mode(caplog):

    with caplog.at_level(logging.WARNING):
        parallel = build_parallel(parallel_mode='unknown_mode')

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'parallel.build' in caplog.records[0].name
    assert 'unknown parallel_mode' in caplog.records[0].msg

    assert 'MultiprocessingDropbox' ==  parallel.communicationChannel.dropbox.__class__.__name__

##__________________________________________________________________||
parallel_modes = ['subprocess', 'htcondor']

@pytest.mark.parametrize('htcondor_job_desc_extra', [[], ['request_memory = 250']])
@pytest.mark.parametrize('user_modules', [[], ['scribblers']])
@pytest.mark.parametrize('processes', [0, 1, 3])
@pytest.mark.parametrize('parallel_mode', parallel_modes)
def test_build_parallel_dropbox(parallel_mode, processes, user_modules,
                        htcondor_job_desc_extra, isatty):

    parallel = build_parallel(
        parallel_mode=parallel_mode,
        processes=processes,
        user_modules=user_modules,
        htcondor_job_desc_extra=htcondor_job_desc_extra
    )

    ## progressMonitor
    assert 'NullProgressMonitor' == parallel.progressMonitor.__class__.__name__

    ## communicationChannel
    assert 'CommunicationChannel' == parallel.communicationChannel.__class__.__name__
    assert 'TaskPackageDropbox' ==  parallel.communicationChannel.dropbox.__class__.__name__

    ## dispatcher
    if parallel_mode == 'subprocess':
        assert 'SubprocessRunner' ==parallel.communicationChannel.dropbox.dispatcher.__class__.__name__
    elif parallel_mode == 'htcondor':
        assert 'HTCondorJobSubmitter' ==parallel.communicationChannel.dropbox.dispatcher.__class__.__name__

    assert 'WorkingArea' == parallel.workingarea.__class__.__name__

    if user_modules:
        assert set(['scribblers', 'alphatwirl']) == set(parallel.workingarea.python_modules)
    else:
        assert set(['alphatwirl']) == set(parallel.workingarea.python_modules)


##__________________________________________________________________||

##__________________________________________________________________||
def test_build_depricated(caplog):
    with caplog.at_level(logging.WARNING):
        parallel = build_parallel_multiprocessing(quiet=True, processes=4)

    progressMonitor = parallel.progressMonitor
    communicationChannel = parallel.communicationChannel
    assert 'NullProgressMonitor' == progressMonitor.__class__.__name__
    assert 'CommunicationChannel' == communicationChannel.__class__.__name__
    assert 'MultiprocessingDropbox' == communicationChannel.dropbox.__class__.__name__

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'parallel.build' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

##__________________________________________________________________||
