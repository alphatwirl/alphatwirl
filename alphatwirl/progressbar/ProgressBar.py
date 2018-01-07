# Tai Sakuma <tai.sakuma@gmail.com>
import time
import sys, collections

##__________________________________________________________________||
class ProgressBar(object):
    def __init__(self):
        self.reports = collections.OrderedDict()
        self.lines = [ ]
        self.interval = 0.1 # [second]
        self._readTime()

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def nreports(self):
        return len(self.reports)

    def present(self, report):
        self.reports[report.taskid] = report
        if not self._need_to_update(report): return
        self._delete_previous_lines()
        self._create_lines()
        self._print_lines()
        self._readTime()

    def _delete_previous_lines(self):
        if len(self.lines) >= 1:
            sys.stdout.write('\b'*len(self.lines[-1]))
        if len(self.lines) >= 2:
            sys.stdout.write('\033M'*(len(self.lines) - 1))
        self.lines = [ ]
        self.last = [ ]

    def _create_lines(self):
        taskids_to_delete = [ ]
        for taskid, report in self.reports.items():
            line = self.createLine(report)
            if report.done >= report.total:
                taskids_to_delete.append(report.taskid)
                self.last.append(line)
            else:
                self.lines.append(line)
        for taskid in taskids_to_delete:
            del self.reports[taskid]

    def _print_lines(self):
        if len(self.last) > 0: sys.stdout.write("\n".join(self.last) + "\n")
        sys.stdout.write("\n".join(self.lines))
        sys.stdout.flush()

    def createLine(self, report):
        nameFieldLength = 32
        percent = float(report.done)/report.total if report.total > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, " ")
        percent = round(percent * 100, 2)
        name = report.name[0:nameFieldLength]
        return " {3:6.2f}% {2:s} | {4:8d} / {5:8d} |:  {0:<{1}s} ".format(name, nameFieldLength, bar, percent, report.done, report.total)

    def _need_to_update(self, report):
        if self._time() - self.lastTime > self.interval: return True
        if report.done == report.total: return True
        if report.done == 0: return True
        return False

    def _time(self): return time.time()
    def _readTime(self): self.lastTime = self._time()

##__________________________________________________________________||
