# Tai Sakuma <tai.sakuma@gmail.com>
import pytest
import sys

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.parallel import build_parallel

##__________________________________________________________________||
@pytest.fixture(
    params=[True, False]
)
def isatty(request, monkeypatch):
    ret = request.param
    org_stdout = sys.stdout
    f = mock.Mock(**{
        'isatty.return_value': ret,
        'write.side_effect': lambda x : org_stdout.write(x)
    })
    monkeypatch.setattr(sys, 'stdout', f)
    return ret

parallel_modes = ['multiprocessing', 'subprocess', 'htcondor']

@pytest.mark.parametrize('htcondor_job_desc_extra', [[], ['request_memory = 250']])
@pytest.mark.parametrize('user_modules', [[], ['scribblers']])
@pytest.mark.parametrize('processes', [0, 1, 3])
@pytest.mark.parametrize('quiet', [True, False])
@pytest.mark.parametrize('parallel_mode', parallel_modes)
def test_build_parallel(parallel_mode, quiet, processes, user_modules,
                        htcondor_job_desc_extra, isatty):

    parallel = build_parallel(
        parallel_mode=parallel_mode,
        quiet=quiet,
        processes=processes,
        user_modules=user_modules,
        htcondor_job_desc_extra=htcondor_job_desc_extra
    )

    ## progressMonitor
    if quiet:
        assert 'NullProgressMonitor' == parallel.progressMonitor.__class__.__name__
    elif parallel_mode in ('subprocess', 'htcondor'):
        assert 'NullProgressMonitor' == parallel.progressMonitor.__class__.__name__
    elif processes == 0:
        assert 'ProgressMonitor' == parallel.progressMonitor.__class__.__name__
    else:
        assert 'BProgressMonitor' == parallel.progressMonitor.__class__.__name__

    ## communicationChannel
    if parallel_mode in ('subprocess', 'htcondor'):
        assert 'CommunicationChannel' == parallel.communicationChannel.__class__.__name__
    elif processes == 0:
        assert 'CommunicationChannel0' == parallel.communicationChannel.__class__.__name__
    else:
        assert 'CommunicationChannel' == parallel.communicationChannel.__class__.__name__

    ## workingarea
    if parallel_mode == 'multiprocessing':
        assert parallel.workingarea is None
    else:
        assert 'WorkingArea' == parallel.workingarea.__class__.__name__
        if user_modules:
            set(['fwtwirl', 'scribblers', 'alphatwirl']) == parallel.workingarea.python_modules
        else:
            set(['fwtwirl', 'alphatwirl']) == parallel.workingarea.python_modules


##__________________________________________________________________||
