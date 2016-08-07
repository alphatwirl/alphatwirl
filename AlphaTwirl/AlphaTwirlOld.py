# Tai Sakuma <tai.sakuma@cern.ch>
import argparse
import sys
import os

from .Configure import TableConfigCompleter
from .HeppyResult import ComponentReaderComposite
from .HeppyResult import ComponentLoop
from .HeppyResult import HeppyResult
from .EventReader import EventReader
from .EventReader import MPEventLoopRunner
from .EventReader import ReaderComposite
from .EventReader import Collector
from .EventReader import NullCollector
from .EventReader import CollectorComposite
from .EventReader import CollectorDelegate
from .Concurrently import CommunicationChannel
from .Concurrently import CommunicationChannel0
from .ProgressBar import ProgressBar
from .ProgressBar import ProgressPrint
from .ProgressBar import ProgressMonitor, BProgressMonitor, NullProgressMonitor
from .Counter import Counter, Count, KeyValueComposer, NextKeyComposer
from .CombineIntoList import CombineIntoList
from .WriteListToFile import WriteListToFile

try:
    from HeppyResult import BEventBuilder as EventBuilder
except ImportError:
    pass

##__________________________________________________________________||
class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, owner, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.owner = owner

    def parse_args(self, *args, **kwargs):
        args = super(ArgumentParser, self).parse_args(*args, **kwargs)
        self.owner.args = args
        return args

##__________________________________________________________________||
def build_progressMonitor_communicationChannel(quiet, processes):

    if quiet:
        progressBar = None
    elif sys.stdout.isatty():
        progressBar = ProgressBar()
    else:
        progressBar = ProgressPrint()

    if processes is None or processes == 0:
        progressMonitor = NullProgressMonitor() if quiet else ProgressMonitor(presentation = progressBar)
        communicationChannel = CommunicationChannel0(progressMonitor)
    else:
        progressMonitor = NullProgressMonitor() if quiet else BProgressMonitor(presentation = progressBar)
        communicationChannel = CommunicationChannel(processes, progressMonitor)

    return progressMonitor, communicationChannel

##__________________________________________________________________||
def buildCounterAndCollector(tblcfg):
    keyValComposer = KeyValueComposer(tblcfg['branchNames'], tblcfg['binnings'], tblcfg['indices'])
    nextKeyComposer = NextKeyComposer(tblcfg['binnings'])
    counter = Counter(
        keyValComposer = keyValComposer,
        summary = tblcfg['countsClass'](),
        nextKeyComposer = nextKeyComposer,
        weightCalculator = tblcfg['weight']
    )
    resultsCombinationMethod = CombineIntoList(keyNames = tblcfg['outColumnNames'], valNames = ('n', 'nvar'))
    deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector0 = Collector(resultsCombinationMethod, deliveryMethod)
    return counter, collector0

##__________________________________________________________________||
def buildReaderAndCollector(preTableReaders, tableConfigs, outDir, force, progressMonitor):
    """
          composite
              |- preTableReader
              |- preTableReader
              |- preTableReader
              |- preTableReader
              |- counter
              |- counter
              |- counter
              |- counter
              |- counter
    """

    tableConfigCompleter = TableConfigCompleter(defaultCountsClass = Count, defaultOutDir = outDir)
    tableConfigs = [tableConfigCompleter.complete(c) for c in tableConfigs]
    if not force: tableConfigs = [c for c in tableConfigs if c['outFile'] and not os.path.exists(c['outFilePath'])]
    if len(tableConfigs) == 0: return None, None
    reader1 = ReaderComposite()
    collector1 = CollectorComposite(progressMonitor.createReporter())

    for reader in preTableReaders:
        reader1.add(reader)
        collector1.add(NullCollector())

    for tblcfg in tableConfigs:
        counter, collector0 = buildCounterAndCollector(tblcfg)
        reader1.add(counter)
        collector1.add(collector0)

    return reader1, collector1

##__________________________________________________________________||
def createTreeReader(analyzerName, fileName, treeName, reader, collector, nevents, maxEventsPerRun, communicationChannel):
    eventLoopRunner = MPEventLoopRunner(communicationChannel)
    eventBuilder = EventBuilder(analyzerName, fileName, treeName, nevents)
    eventReader = EventReader(eventBuilder, eventLoopRunner, reader, collector, maxEventsPerRun)
    return eventReader

##__________________________________________________________________||
class AlphaTwirlOld(object):

    def __init__(self):
        self.args = None
        self.componentReaders = ComponentReaderComposite()
        self.treeReaderConfigs = [ ]

    def ArgumentParser(self, *args, **kwargs):
        parser = ArgumentParser(self, *args, **kwargs)
        parser = self._add_arguments(parser)
        return parser

    def _add_arguments(self, parser):
        parser.add_argument('-i', '--heppydir', default = '/Users/sakuma/work/cms/c150130_RA1_data/74X/MC/20150713_MC/20150713_SingleMu', action = 'store', help = "Heppy results dir")
        parser.add_argument("-p", "--processes", action = "store", default = None, type = int, help = "number of processes to run in parallel")
        parser.add_argument("-q", "--quiet", action = "store_true", default = False, help = "quiet mode")
        parser.add_argument('-o', '--outDir', default = 'tbl/out', action = 'store')
        parser.add_argument("-n", "--nevents", action = "store", default = -1, type = int, help = "maximum number of events to process for each component")
        parser.add_argument("--max-events-per-process", action = "store", default = -1, type = int, help = "maximum number of events per process")
        parser.add_argument("-c", "--components", default = None, nargs = '*', help = "the list of components")
        parser.add_argument("--force", action = "store_true", default = False, dest="force", help = "recreate all output files")
        return parser

    def addComponentReader(self, reader):
        self.componentReaders.add(reader)

    def addTreeReader(self, analyzerName, fileName, treeName,
                      preTableReaders = [ ], tableConfigs = [ ]):

        cfg = dict(
            analyzerName = analyzerName,
            fileName = fileName,
            treeName = treeName,
            preTableReaders = preTableReaders,
            tableConfigs = tableConfigs,
            )

        self.treeReaderConfigs.append(cfg)

    def _build(self):

        if self.args is None: self.ArgumentParser().parse_args()

        self.progressMonitor, self.communicationChannel = build_progressMonitor_communicationChannel(self.args.quiet, self.args.processes)

        for cfg in self.treeReaderConfigs:
            reader, collector = buildReaderAndCollector(
                preTableReaders = cfg['preTableReaders'],
                tableConfigs = cfg['tableConfigs'],
                outDir = self.args.outDir,
                force = self.args.force,
                progressMonitor = self.progressMonitor,
            )
            if reader is None: continue
            treeReader = createTreeReader(
                analyzerName = cfg['analyzerName'],
                fileName = cfg['fileName'],
                treeName = cfg['treeName'],
                reader = reader,
                collector = collector,
                nevents = self.args.nevents,
                maxEventsPerRun = self.args.max_events_per_process,
                communicationChannel = self.communicationChannel,
            )
            self.addComponentReader(treeReader)

        if self.args.components == ['all']: self.args.components = None
        heppyResult = HeppyResult(path = self.args.heppydir, componentNames = self.args.components)
        componentLoop = ComponentLoop(heppyResult, self.componentReaders)
        return componentLoop

    def run(self):
        loop = self._build()
        self.progressMonitor.begin()
        self.communicationChannel.begin()
        loop()
        self.communicationChannel.end()
        self.progressMonitor.end()

##__________________________________________________________________||
