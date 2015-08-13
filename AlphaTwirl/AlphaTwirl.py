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
from .EventReader import ReaderWithEventSelection
from .EventReader import Collector
from .EventReader import NullCollector
from .EventReader import CollectorComposite
from .EventReader import CollectorDelegate
from .Concurrently import CommunicationChannel
from .Concurrently import CommunicationChannel0
from .ProgressBar import ProgressBar
from .ProgressBar import ProgressMonitor, BProgressMonitor, NullProgressMonitor
from .Counter import Counter, Counts, GenericKeyComposerB, NextKeyComposer
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
def buildReaderAndCollector(scribblers, eventSelection, tableConfigs, outDir, force, progressMonitor):
    """
        1:composite
              |- scribble
              |- scribble
              |- scribble
              |- 2:selection - 3:composite
              |                      |- counter
              |                      |- counter
              |                      |- counter
              |                      |- counter
              |                      |- counter
              |
    """

    tableConfigCompleter = TableConfigCompleter(defaultCountsClass = Counts, defaultOutDir = outDir)
    tableConfigs = [tableConfigCompleter.complete(c) for c in tableConfigs]
    if not force: tableConfigs = [c for c in tableConfigs if c['outFile'] and not os.path.exists(c['outFilePath'])]
    if len(tableConfigs) == 0: return None, None
    reader1 = ReaderComposite()
    collector1 = CollectorComposite(progressMonitor.createReporter())

    for scribbler in scribblers:
        reader1.add(scribbler)
        collector1.add(NullCollector())

    reader3 = ReaderComposite()
    collector3 = CollectorComposite(progressMonitor.createReporter())
    if eventSelection is not None:
        reader2 = ReaderWithEventSelection(reader3, eventSelection)
        collector2 = CollectorDelegate(collector3)
        reader1.add(reader2)
        collector1.add(collector2)
    else:
        reader1.add(reader3)
        collector1.add(collector3)

    for tblcfg in tableConfigs:
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
        reader3.add(counter)
        collector3.add(collector0)


    return reader1, collector1

##__________________________________________________________________||
def createTreeReader(analyzerName, fileName, treeName, reader, collector, nevents, communicationChannel):
    eventLoopRunner = MPEventLoopRunner(communicationChannel)
    eventBuilder = EventBuilder(analyzerName, fileName, treeName, nevents)
    eventReader = EventReader(eventBuilder, eventLoopRunner, reader, collector)
    return eventReader

##__________________________________________________________________||
class AlphaTwirl(object):

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
        parser.add_argument("-c", "--components", default = None, nargs = '*', help = "the list of components")
        parser.add_argument("--force", action = "store_true", default = False, dest="force", help = "recreate all output files")
        return parser

    def addComponentReader(self, reader):
        self.componentReaders.add(reader)

    def addTreeReader(self, analyzerName, fileName, treeName, scribblers = [ ],
                      tableConfigs = [ ], eventSelection = None):
        cfg = dict(
            analyzerName = analyzerName,
            fileName = fileName,
            treeName = treeName,
            scribblers = scribblers,
            tableConfigs = tableConfigs,
            eventSelection = eventSelection
            )

        self.treeReaderConfigs.append(cfg)

    def _build(self):

        self.progressBar = None if self.args.quiet else ProgressBar()
        if self.args.processes is None or self.args.processes == 0:
            self.progressMonitor = NullProgressMonitor() if self.args.quiet else ProgressMonitor(presentation = self.progressBar)
            self.communicationChannel = CommunicationChannel0(self.progressMonitor)
        else:
            self.progressMonitor = NullProgressMonitor() if self.args.quiet else BProgressMonitor(presentation = self.progressBar)
            self.communicationChannel = CommunicationChannel(self.args.processes, self.progressMonitor)

        for cfg in self.treeReaderConfigs:
            reader, collector = buildReaderAndCollector(
                scribblers = cfg['scribblers'],
                eventSelection = cfg['eventSelection'],
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
                communicationChannel = self.communicationChannel,
            )
            self.addComponentReader(treeReader)

    def run(self):
        if self.args is None: self.ArgumentParser().parse_args()
        self._build()
        self.progressMonitor.begin()
        self.communicationChannel.begin()
        componentLoop = ComponentLoop(self.componentReaders)
        if self.args.components == ['all']: self.args.components = None
        heppyResult = HeppyResult(path = self.args.heppydir, componentNames = self.args.components)
        componentLoop(heppyResult.components())
        self.communicationChannel.end()
        self.progressMonitor.end()

##__________________________________________________________________||
