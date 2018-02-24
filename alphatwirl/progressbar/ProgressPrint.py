# Tai Sakuma <tai.sakuma@gmail.com>
import time
import sys, collections

##__________________________________________________________________||
class ProgressPrint(object):
    def __init__(self):
        self.reports = collections.OrderedDict()
        self.lines = [ ]
        self.interval = 60.0 # [second]
        self._readTime()
        self.last = [ ]

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def nreports(self):
        return len(self.reports)

    def present(self, report):
        self.reports[report.taskid] = report
        if not self._need_to_update(report): return
        self._create_lines()
        self._print_lines()
        self._readTime()

    def _create_lines(self):
        self.lines = [ ]
        for taskid, report in self.reports.items():
            line = self.createLine(report)
            if report.done >= report.total:
                del self.reports[report.taskid]
                self.last.append(line)
            else:
                self.lines.append(line)

    def _print_lines(self):
        sys.stdout.write("\n")
        sys.stdout.write(time.asctime(time.localtime(time.time())))
        sys.stdout.write("\n")
        if len(self.last) > 0: sys.stdout.write("\n".join(self.last) + "\n")
        sys.stdout.write("\n".join(self.lines) + "\n")
        sys.stdout.flush()

    def createLine(self, report):
        percent = float(report.done)/report.total if report.total > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, " ")
        percent = round(percent * 100, 2)
        return " {1:8d} / {2:8d} ({0:6.2f}%) {3} ".format(percent, report.done, report.total, report.name)

    def _need_to_update(self, report):
        if self._time() - self.lastTime > self.interval: return True
        if report.done == report.total: return True
        if report.done == 0: return True
        return False

    def _time(self): return time.time()
    def _readTime(self): self.lastTime = self._time()

##__________________________________________________________________||
