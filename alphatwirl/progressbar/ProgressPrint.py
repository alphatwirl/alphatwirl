# Tai Sakuma <tai.sakuma@gmail.com>
import time
import sys, collections

##__________________________________________________________________||
class ProgressPrint(object):
    def __init__(self):

        self._new_taskids = [ ]
        self._active_taskids = [ ] # in order of arrival
        self._finishing_taskids = [ ]
        self._complete_taskids = [ ] # in order of completion
        self._report_dict = { }

        self.lines = [ ]
        ## self.interval = 60.0 # [second]
        self.last = [ ]

        self.interval = 1.0 # [second]
        self._read_time()

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def nreports(self):
        return len(self._active_taskids)

    def present(self, report):

        if not self._register_report(report):
            return

        if not self._need_to_present(report):
            return

        self._present()

        self._update_registry()

        self._read_time()

    def _register_report(self, report):

        if report.taskid in self._complete_taskids:
            return False

        self._report_dict[report.taskid] = report

        if report.taskid in self._finishing_taskids:
            return True

        if report.last():
            try:
                self._active_taskids.remove(report.taskid)
            except ValueError:
                pass

            try:
                self._new_taskids.remove(report.taskid)
            except ValueError:
                pass

            self._finishing_taskids.append(report.taskid)

            return True

        if report.taskid in self._active_taskids:
            return True

        if report.taskid in self._new_taskids:
            return True

        self._new_taskids.append(report.taskid)
        return True

    def _update_registry(self):
        self._active_taskids.extend(self._new_taskids)
        del self._new_taskids[:]

        self._complete_taskids.extend(self._finishing_taskids)
        del self._finishing_taskids[:]

    def _need_to_present(self, report):

        if self._new_taskids:
            return True

        if self._finishing_taskids:
            return True

        if self._time() - self.last_time > self.interval:
            return True

        return False

    def _present(self):
        self._create_lines()
        self._print_lines()

    def _create_lines(self):

        self.lines = [ ]
        for taskid in self._active_taskids + self._new_taskids:
            report = self._report_dict[taskid]
            line = self._create_line(report)
            self.lines.append(line)

        for taskid in self._finishing_taskids:
            report = self._report_dict[taskid]
            line = self._create_line(report)
            self.last.append(line)

    def _print_lines(self):
        sys.stdout.write("\n")
        sys.stdout.write(time.asctime(time.localtime(time.time())))
        sys.stdout.write("\n")
        if len(self.last) > 0: sys.stdout.write("\n".join(self.last) + "\n")
        sys.stdout.write("\n".join(self.lines) + "\n")
        sys.stdout.flush()

    def _create_line(self, report):
        percent = float(report.done)/report.total if report.total > 0 else 1
        percent = round(percent * 100, 2)
        return " {1:8d} / {2:8d} ({0:6.2f}%) {3} ".format(percent, report.done, report.total, report.name)

    def _time(self):
        return time.time()

    def _read_time(self):
        self.last_time = self._time()

##__________________________________________________________________||
