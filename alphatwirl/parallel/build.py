# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging

from alphatwirl import concurrently, progressbar

from .parallel import Parallel

##__________________________________________________________________||
def build_parallel(parallel_mode, quiet=True, processes=4, user_modules=[ ],
                   htcondor_job_desc_extra=[ ]):

    default_parallel_mode = 'multiprocessing'

    if parallel_mode in ('subprocess', 'htcondor'):
        return build_parallel_dropbox(
            parallel_mode=parallel_mode,
            user_modules=user_modules,
            htcondor_job_desc_extra=htcondor_job_desc_extra
        )

    if not parallel_mode == default_parallel_mode:
        logger = logging.getLogger(__name__)
        logger.warning('unknown parallel_mode "{}", use default "{}"'.format(
            parallel_mode, default_parallel_mode
        ))

    return build_parallel_multiprocessing(quiet=quiet, processes=processes)

##__________________________________________________________________||
def build_parallel_dropbox(parallel_mode, user_modules,
                           htcondor_job_desc_extra=[ ]):
    tmpdir = '_ccsp_temp'
    user_modules = set(user_modules)
    user_modules.add('alphatwirl')
    progressMonitor = progressbar.NullProgressMonitor()
    if parallel_mode == 'htcondor':
        dispatcher = concurrently.HTCondorJobSubmitter(job_desc_extra=htcondor_job_desc_extra)
    else:
        dispatcher = concurrently.SubprocessRunner()
    workingarea = concurrently.WorkingArea(
        dir=tmpdir,
        python_modules=list(user_modules)
    )
    dropbox = concurrently.TaskPackageDropbox(
        workingArea=workingarea,
        dispatcher=dispatcher
    )
    communicationChannel = concurrently.CommunicationChannel(
        dropbox=dropbox
    )
    return Parallel(progressMonitor, communicationChannel, workingarea)

##__________________________________________________________________||
def build_parallel_multiprocessing(quiet, processes):

    if quiet:
        progressBar = None
    elif sys.stdout.isatty():
        progressBar = progressbar.ProgressBar()
    else:
        progressBar = progressbar.ProgressPrint()

    if processes is None or processes == 0:
        progressMonitor = progressbar.NullProgressMonitor() if quiet else progressbar.ProgressMonitor(presentation = progressBar)
        communicationChannel = concurrently.CommunicationChannel0()
    else:
        progressMonitor = progressbar.NullProgressMonitor() if quiet else progressbar.BProgressMonitor(presentation = progressBar)
        dropbox = concurrently.MultiprocessingDropbox(processes, progressMonitor)
        communicationChannel = concurrently.CommunicationChannel(dropbox = dropbox)

    return Parallel(progressMonitor, communicationChannel)

##__________________________________________________________________||
