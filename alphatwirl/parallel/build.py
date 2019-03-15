# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging

import atpbar

from alphatwirl import concurrently
from alphatwirl.misc.removal import _removed, _removed_func_option

from .parallel import Parallel

##__________________________________________________________________||
@_removed_func_option('htcondor_job_desc_extra', msg='use dispatcher_options instead')
def build_parallel(parallel_mode, quiet=True, processes=4,
                   user_modules=None, dispatcher_options=None):
    """initializes `Parallel`

    Parameters
    ----------
    parallel_mode : str
        "multiprocessing" (default), "htcondor" or "subprocess"
    quiet : bool, optional
        if True, progress bars will not be shown in the "multiprocessing" mode.
    process : int, optional
        The number of processes when ``parallel_mode`` is
        "multiprocessing"
    user_modules : list, optional
        The names of modules to be sent to worker nodes when
        parallel_mode is "htcondor"
    dispatcher_options : dict, optional
        Options to dispatcher

    Returns
    -------
    parallel
        an instance of the class `Parallel`

    """

    if user_modules is None:
        user_modules = [ ]

    if dispatcher_options is None:
        dispatcher_options = dict()

    dispatchers = ('subprocess', 'htcondor')
    parallel_modes = ('multiprocessing', ) + dispatchers
    default_parallel_mode = 'multiprocessing'

    if not parallel_mode in parallel_modes:
        logger = logging.getLogger(__name__)
        logger.warning('unknown parallel_mode "{}", use default "{}"'.format(
            parallel_mode, default_parallel_mode
        ))
        parallel_mode = default_parallel_mode

    if parallel_mode == 'multiprocessing':
        if quiet:
            atpbar.disable()
        return _build_parallel_multiprocessing(processes=processes)

    return _build_parallel_dropbox(
        parallel_mode=parallel_mode,
        user_modules=user_modules,
        dispatcher_options=dispatcher_options
    )

##__________________________________________________________________||
def _build_parallel_dropbox(parallel_mode, user_modules,
                            dispatcher_options):

    workingarea_topdir = '_ccsp_temp'
    python_modules = set(user_modules)
    python_modules.add('alphatwirl')
    python_modules.add('atpbar')
    python_modules.add('mantichora')
    workingarea_options = dict(topdir=workingarea_topdir, python_modules=python_modules)

    if parallel_mode == 'htcondor':
        dispatcher_class = concurrently.HTCondorJobSubmitter
    else:
        dispatcher_class = concurrently.SubprocessRunner

    return _build_parallel_dropbox_(
        workingarea_options, dispatcher_class, dispatcher_options
    )

def _build_parallel_dropbox_(workingarea_options,
                             dispatcher_class, dispatcher_options):

    workingarea = concurrently.WorkingArea(**workingarea_options)

    dispatcher = dispatcher_class(**dispatcher_options)

    dropbox = concurrently.TaskPackageDropbox(
        workingArea=workingarea,
        dispatcher=dispatcher
    )
    communicationChannel = concurrently.CommunicationChannel(
        dropbox=dropbox
    )

    return Parallel(None, communicationChannel, workingarea)

##__________________________________________________________________||
def _build_parallel_multiprocessing(processes):

    if processes is None or processes == 0:
        communicationChannel = concurrently.CommunicationChannel0()
    else:
        dropbox = concurrently.MultiprocessingDropbox(processes)
        communicationChannel = concurrently.CommunicationChannel(dropbox=dropbox)
    return Parallel(None, communicationChannel)

##__________________________________________________________________||
# deprecated at v0.15.0 (2018-02-28)
# removed after v0.23.2 (2019-02-27)
@_removed(msg='use alphatwirl.parallel.build.build_parallel() instead.')
def build_parallel_multiprocessing(quiet, processes):
    pass

##__________________________________________________________________||
