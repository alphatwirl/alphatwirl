# Tai Sakuma <sakuma@fnal.gov>
import sys, collections

##____________________________________________________________________________||
class ProgressBar2(object):
    def __init__(self):
        self._progress = collections.OrderedDict()
        self._finished = collections.OrderedDict()

    def nreports(self):
        return len(self._progress)

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
        bar = ('=' * int(percent * 40)).ljust(40)
        percent = int(percent * 100)
        sys.stdout.write("%35s [%s] %3s%% %7d / %7d\n" % (name, bar, percent, report.done, report.total))

##____________________________________________________________________________||
class ProgressBar(object):
    def __init__(self):
        self.reports = collections.OrderedDict()
        self.lines = [ ]

    def nreports(self):
        return len(self.reports)

    def present(self, report):
        self.reports[report.name] = report

        # delete previous lines
        if len(self.lines) >= 1:
            sys.stdout.write('\b'*len(self.lines[-1]))
        if len(self.lines) >= 2:
            sys.stdout.write('\033M'*(len(self.lines) - 1))
        self.lines = [ ]
        last = [ ]

        # create lines
        for name, report in self.reports.items():
            line = self.createLine(name, report)
            if report.done >= report.total:
                del self.reports[report.name]
                last.append(line)
            else:
                self.lines.append(line)

        # print lines
        if len(last) > 0: sys.stdout.write("\n".join(last) + "\n")
        sys.stdout.write("\n".join(self.lines))
        sys.stdout.flush()

    def createLine(self, name, report):
        percent = float(report.done)/report.total
        bar = ('=' * int(percent * 40)).ljust(40)
        percent = round(percent * 100, 2)
        return "{0:>35s} [{1:s}] {2:6.2f}% {3:7d} / {4:7d}".format(name, bar, percent, report.done, report.total)

##____________________________________________________________________________||
