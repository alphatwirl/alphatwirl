# Tai Sakuma <tai.sakuma@cern.ch>
import sys

from .. import ProgressBar
from .. import Concurrently

##__________________________________________________________________||
def build_progressMonitor_communicationChannel(quiet, processes):

    if quiet:
        progressBar = None
    elif sys.stdout.isatty():
        progressBar = ProgressBar.ProgressBar()
    else:
        progressBar = ProgressBar.ProgressPrint()

    if processes is None or processes == 0:
        progressMonitor = ProgressBar.NullProgressMonitor() if quiet else ProgressBar.ProgressMonitor(presentation = progressBar)
        communicationChannel = Concurrently.CommunicationChannel0(progressMonitor)
    else:
        progressMonitor = ProgressBar.NullProgressMonitor() if quiet else ProgressBar.BProgressMonitor(presentation = progressBar)
        dropbox = Concurrently.MultiprocessingDropbox(processes, progressMonitor)
        communicationChannel = Concurrently.CommunicationChannel(dropbox = dropbox)

    return progressMonitor, communicationChannel

##__________________________________________________________________||
