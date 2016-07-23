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
from .Counter import Counter, Counts, GenericKeyComposerB, NextKeyComposer
from .CombineIntoList import CombineIntoList
from .WriteListToFile import WriteListToFile

try:
    from HeppyResult import BEventBuilder as EventBuilder
except ImportError:
    pass

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
    keyComposer = GenericKeyComposerB(tblcfg['branchNames'], tblcfg['binnings'], tblcfg['indices'])
    nextKeyComposer = NextKeyComposer(tblcfg['binnings'])
    counter = Counter(
        keyComposer = keyComposer,
        countMethod = tblcfg['countsClass'](),
        nextKeyComposer = nextKeyComposer,
        weightCalculator = tblcfg['weight']
    )
    resultsCombinationMethod = CombineIntoList(keyNames = tblcfg['outColumnNames'])
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

    tableConfigCompleter = TableConfigCompleter(defaultCountsClass = Counts, defaultOutDir = outDir)
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
config_default = dict(
    heppydir = '/Users/sakuma/work/cms/c150130_RA1_data/80X/MC/20160708_B01_MCMiniAODv2_SM/AtLogic_MCMiniAODv2_SM',
    processes = None,
    quiet = False,
    outDir = 'tbl/out',
    nevents = -1,
    max_events_per_process = -1,
    components = None,
    force = False
)

##__________________________________________________________________||
class AlphaTwirlConfigurerFromArgs():

    def __init__(self):
        self.cfg = config_default.copy()

    def add_arguments(self, parser):
        parser.add_argument('-i', '--heppydir', default = self.cfg['heppydir'], help = 'Heppy results dir')
        parser.add_argument('-p', '--processes', default = self.cfg['processes'], type = int, help = 'number of processes to run in parallel')
        parser.add_argument('-q', '--quiet', action = 'store_true', default = self.cfg['quiet'], help = 'quiet mode')
        parser.add_argument('-o', '--outDir', default = 'tbl/out')
        parser.add_argument('-n', '--nevents', default = -1, type = int, help = 'maximum number of events to process for each component')
        parser.add_argument('--max-events-per-process', default = -1, type = int, help = 'maximum number of events per process')
        parser.add_argument('-c', '--components', default = None, nargs = '*', help = 'the list of components')
        parser.add_argument('--force', action = 'store_true', default = False, dest='force', help = 'recreate all output files')

    def configure(self, args):
        self.cfg.update(vars(args))
        return self.cfg.copy()

##__________________________________________________________________||
class AlphaTwirl(object):

    def __init__(self, config = None):
        self.componentReaders = ComponentReaderComposite()
        self.treeReaderConfigs = [ ]

        self.cfg = config if config is not None else config_default.copy()

        self.progressMonitor, self.communicationChannel = build_progressMonitor_communicationChannel(self.cfg['quiet'], self.cfg['processes'])
        self.progressMonitor.begin()
        self.communicationChannel.begin()

    def addComponentReader(self, reader):
        self.componentReaders.add(reader)

    def addTreeReader(self, analyzerName, fileName, treeName,
                      preTableReaders = [ ], tableConfigs = [ ]):

        reader, collector = buildReaderAndCollector(
            preTableReaders = preTableReaders,
            tableConfigs = tableConfigs,
            outDir = self.cfg['outDir'],
            force = self.cfg['force'],
            progressMonitor = self.progressMonitor,
        )
        if reader is None: return

        eventLoopRunner = MPEventLoopRunner(self.communicationChannel)
        eventBuilder = EventBuilder(analyzerName, fileName, treeName, self.cfg['nevents'])
        eventReader = EventReader(eventBuilder, eventLoopRunner, reader, collector, self.cfg['max_events_per_process'])
        self.addComponentReader(eventReader)

    def _build(self):

        if self.cfg['components'] == ['all']: self.cfg['components'] = None
        heppyResult = HeppyResult(path = self.cfg['heppydir'], componentNames = self.cfg['components'])
        componentLoop = ComponentLoop(heppyResult, self.componentReaders)
        return componentLoop

    def run(self):
        loop = self._build()
        loop()

    def end(self):
        self.communicationChannel.end()
        self.progressMonitor.end()

##__________________________________________________________________||
