# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import ProgressReport

##__________________________________________________________________||
class EventReaderComposite(object):

    """A composite of event readers"

    """

    def __init__(self):
        self.readers = []

    def add(self, reader):
        self.readers.append(reader)

    def begin(self, event):
        for reader in self.readers: reader.begin(event)

    def event(self, event):
        for reader in self.readers: reader.event(event)

    def end(self):
        for reader in self.readers: reader.end()

    def setResults(self, results):
        for reader, result in zip(self.readers, results):
            reader.setResults(result)

    def results(self):
        return [reader.results() for reader in self.readers]

##__________________________________________________________________||
class EventReaderPackageBundle(object):

    def __init__(self, progressBar = None):
        self._packages = [ ]
        self.progressBar = progressBar

    def add(self, package):
        self._packages.append(package)

    def make(self, datasetName):
        readerComposite = EventReaderComposite()
        for package in self._packages:
            reader = package.make(datasetName)
            readerComposite.add(reader)
        return readerComposite

    def collect(self):
        for i, package in enumerate(self._packages):
            if self.progressBar is not None:
                report = ProgressReport(name = "collecting results", done = i + 1, total = len(self._packages))
                self.progressBar.present(report)
            package.collect()


##__________________________________________________________________||
