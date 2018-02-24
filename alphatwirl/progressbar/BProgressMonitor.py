# Tai Sakuma <tai.sakuma@gmail.com>
import multiprocessing

from .ProgressReporter import ProgressReporter
from .ProgressReportPickup import ProgressReportPickup

import alphatwirl

##__________________________________________________________________||
class BProgressMonitor(object):
    """A progress monitor of tasks.

    This class monitors the progress of tasks and present it.

    Tasks can be concurrently executed. The progress can be presented
    in an arbitrary way specified at the initialization.

    This class monitors the progress and present it in the background
    by using `ProgressReportPickup`.

    In order for a progress to be monitored by this class, an object
    that executes a task needs to send the `ProgressReport` through
    the `ProgressReporter` created by this class.

    Examples:

      A presentation method needs to be specified at the
      initialization. For example, to use `ProgressBar`::

        presentation = ProgressBar()
        monitor = BProgressMonitor(presentation)

      After the initialization, start monitoring::

        monitor.begin()

      Then, create as many reporters (`ProgressReporter`) as the
      number of the tasks whose progresses need to be monitored::

        reporter1 = monitor.createReporter()
        reporter2 = monitor.createReporter()
        reporter3 = monitor.createReporter()

      These reporters can be given to objects which execute the tasks.
      These objects can be in other processes as long as the reporters
      are properly passed to them.

      If a `ProgressReport` is given to these reporters::

        reporter1.report(report)

      the report will be received by `ProgressReportPickup`, which
      will use the report to present the progress in the way
      specified.

      When all tasks are finished, end monitoring::

        monitor.end()

      This will ends `ProgressReportPickup`, which is running in a
      different process.

    """

    def __init__(self, presentation):
        self.queue = multiprocessing.Queue()
        self.presentation = presentation

    def __repr__(self):
        return '{}(presentation={!r})'.format(
            self.__class__.__name__,
            self.presentation
        )

    def begin(self):
        self.pickup = ProgressReportPickup(self.queue, self.presentation)
        self.pickup.start()
        reporter = self.createReporter()
        alphatwirl.progressbar._progress_reporter = reporter

    def end(self):
        alphatwirl.progressbar._progress_reporter = None
        self.queue.put(None)
        self.pickup.join()

    def createReporter(self):
        return ProgressReporter(queue=self.queue)

##__________________________________________________________________||
