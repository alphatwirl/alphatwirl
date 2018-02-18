# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging
import alphatwirl

from .parallel import Parallel

##__________________________________________________________________||
def build_parallel(parallel_mode, quiet=True, processes=4, user_modules=[ ],
                   htcondor_job_desc_extra=[ ]):

    default_parallel_mode = 'multiprocessing'

    if parallel_mode in ('subprocess', 'htcondor'):
        return build_parallel_dropbox(
            parallel_mode=parallel_mode,
            quiet=quiet,
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
def build_parallel_dropbox(parallel_mode, quiet, user_modules,
                           htcondor_job_desc_extra=[ ]):
    tmpdir = '_ccsp_temp'
    user_modules = set(user_modules)
    user_modules.add('fwtwirl')
    user_modules.add('alphatwirl')
    alphatwirl.mkdir_p(tmpdir)
    progressMonitor = alphatwirl.progressbar.NullProgressMonitor()
    if parallel_mode == 'htcondor':
        dispatcher = alphatwirl.concurrently.HTCondorJobSubmitter(job_desc_extra=htcondor_job_desc_extra)
    else:
        dispatcher = alphatwirl.concurrently.SubprocessRunner()
    workingarea = alphatwirl.concurrently.WorkingArea(
        dir=tmpdir,
        python_modules=list(user_modules)
    )
    dropbox = alphatwirl.concurrently.TaskPackageDropbox(
        workingArea=workingarea,
        dispatcher=dispatcher
    )
    communicationChannel = alphatwirl.concurrently.CommunicationChannel(
        dropbox=dropbox
    )
    return Parallel(progressMonitor, communicationChannel, workingarea)

##__________________________________________________________________||
def build_parallel_multiprocessing(quiet, processes):

    if quiet:
        progressBar = None
    elif sys.stdout.isatty():
        progressBar = alphatwirl.progressbar.ProgressBar()
    else:
        progressBar = alphatwirl.progressbar.ProgressPrint()

    if processes is None or processes == 0:
        progressMonitor = alphatwirl.progressbar.NullProgressMonitor() if quiet else alphatwirl.progressbar.ProgressMonitor(presentation = progressBar)
        communicationChannel = alphatwirl.concurrently.CommunicationChannel0(progressMonitor)
    else:
        progressMonitor = alphatwirl.progressbar.NullProgressMonitor() if quiet else alphatwirl.progressbar.BProgressMonitor(presentation = progressBar)
        dropbox = alphatwirl.concurrently.MultiprocessingDropbox(processes, progressMonitor)
        communicationChannel = alphatwirl.concurrently.CommunicationChannel(dropbox = dropbox)

    return Parallel(progressMonitor, communicationChannel)

##__________________________________________________________________||
