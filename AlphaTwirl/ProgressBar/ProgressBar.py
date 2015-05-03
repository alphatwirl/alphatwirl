# Tai Sakuma <tai.sakuma@cern.ch>
import sys, collections

##____________________________________________________________________________||
class ProgressBar(object):
    def __init__(self):
        self.reports = collections.OrderedDict()
        self.lines = [ ]

    def nreports(self):
        return len(self.reports)

    def present(self, report):
        self.reports[report.taskid] = report

        # delete previous lines
        if len(self.lines) >= 1:
            sys.stdout.write('\b'*len(self.lines[-1]))
        if len(self.lines) >= 2:
            sys.stdout.write('\033M'*(len(self.lines) - 1))
        self.lines = [ ]
        last = [ ]

        # create lines
        for taskid, report in self.reports.items():
            line = self.createLine(report)
            if report.done >= report.total:
                del self.reports[report.taskid]
                last.append(line)
            else:
                self.lines.append(line)

        # print lines
        if len(last) > 0: sys.stdout.write("\n".join(last) + "\n")
        sys.stdout.write("\n".join(self.lines))
        sys.stdout.flush()

    def createLine(self, report):
        nameFieldLength = 32
        percent = float(report.done)/report.total if report.total > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, " ")
        percent = round(percent * 100, 2)
        name = report.name[0:nameFieldLength]
        return " {3:6.2f}% {2:s} | {4:7d} / {5:7d} |:  {0:<{1}s} ".format(name, nameFieldLength, bar, percent, report.done, report.total)

##____________________________________________________________________________||
