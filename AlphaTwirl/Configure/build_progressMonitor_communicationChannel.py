# Tai Sakuma <tai.sakuma@cern.ch>
import sys

from ..ProgressBar import ProgressBar
from ..ProgressBar import ProgressPrint
from ..ProgressBar import ProgressMonitor, BProgressMonitor, NullProgressMonitor
from ..Concurrently import CommunicationChannel
from ..Concurrently import CommunicationChannel0

##__________________________________________________________________||
def build_progressMonitor_communicationChannel(quiet, processes):

    if quiet:
        progressBar = None
    elif sys.stdout.isatty():
        progressBar = ProgressBar()
    else:
        progressBar = ProgressPrint()

    if processes is None or processes == 0:
        progressMonitor = NullProgressMonitor() if quiet else ProgressMonitor(presentation = progressBar)
        communicationChannel = CommunicationChannel0(progressMonitor)
    else:
        progressMonitor = NullProgressMonitor() if quiet else BProgressMonitor(presentation = progressBar)
        communicationChannel = CommunicationChannel(processes, progressMonitor)

    return progressMonitor, communicationChannel

##__________________________________________________________________||
