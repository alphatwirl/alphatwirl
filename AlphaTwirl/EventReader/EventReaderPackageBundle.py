# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import ProgressReport

##__________________________________________________________________||
class EventReaderPackageBundle(object):

    def __init__(self, progressBar = None):
        self._packages = [ ]
        self.progressBar = progressBar

    def add(self, package):
        self._packages.append(package)

    def make(self, datasetName):
        readers = [package.make(datasetName) for package in self._packages]
        return readers

    def collect(self):
        for i, package in enumerate(self._packages):
            if self.progressBar is not None:
                report = ProgressReport(name = "collecting results", done = i + 1, total = len(self._packages))
                self.progressBar.present(report)
            package.collect()


##__________________________________________________________________||
