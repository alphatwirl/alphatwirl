# Tai Sakuma <sakuma@fnal.gov>
import sys, collections

##____________________________________________________________________________||
class ProgressBar(object):
    def __init__(self):
        self._progress = collections.OrderedDict()

    def present(self, report):
        self._progress[report.name] = report
        sys.stdout.write('\033[2J\033[H') #clear screen
        for name, report in self._progress.items():
            percent = float(report.done)/report.total
            bar = ('=' * int(percent * 20)).ljust(20)
            percent = int(percent * 100)
            sys.stdout.write("%30s [%s] %3s%% %7d / %7d\n" % (name, bar, percent, report.done, report.total))
        sys.stdout.flush()

##____________________________________________________________________________||
