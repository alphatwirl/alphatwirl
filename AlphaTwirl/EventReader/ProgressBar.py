# Tai Sakuma <sakuma@fnal.gov>
import sys, collections

##____________________________________________________________________________||
class ProgressBar(object):
    def __init__(self):
        self._progress = collections.OrderedDict()
        self._finished = collections.OrderedDict()

    def present(self, report):
        self._progress[report.name] = report
        sys.stdout.write('\033[2J\033[H') #clear screen
        for name, report in self._finished.items():
            self._presentFor(name, report)
        for name, report in self._progress.items():
            self._presentFor(name, report)
            if report.done >= report.total:
                del self._progress[report.name]
                self._finished[report.name] = report
        sys.stdout.flush()

    def _presentFor(self, name, report):
        percent = float(report.done)/report.total
        bar = ('=' * int(percent * 20)).ljust(20)
        percent = int(percent * 100)
        sys.stdout.write("%30s [%s] %3s%% %7d / %7d\n" % (name, bar, percent, report.done, report.total))

##____________________________________________________________________________||
