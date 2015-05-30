# Tai Sakuma <tai.sakuma@cern.ch>
import argparse
import sys
import os
import itertools

from HeppyResult import ComponentReaderComposite
from HeppyResult import ComponentLoop
from HeppyResult import HeppyResult
from EventReader import EventReaderBundle
from EventReader import EventReaderCollectorAssociator
from EventReader import EventReaderCollectorAssociatorComposite
from EventReader import EventLoopRunner
from EventReader import MPEventLoopRunner
from Concurrently import CommunicationChannel
from ProgressBar import ProgressBar
from ProgressBar import ProgressMonitor, BProgressMonitor, NullProgressMonitor
from Counter import Counts
from Counter import GenericKeyComposerBFactory
from Counter import CounterFactory
from CombineIntoList import CombineIntoList
from WriteListToFile import WriteListToFile
from EventReader import Collector

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
defaultCountsClass = Counts

##__________________________________________________________________||
def completeTableConfig(tblcfg, outDir = None):
    if 'outColumnNames' not in tblcfg: tblcfg['outColumnNames'] = tblcfg['branchNames']
    if 'indices' not in tblcfg: tblcfg['indices'] = None
    if 'countsClass' not in tblcfg: tblcfg['countsClass'] = defaultCountsClass
    if 'outFile' not in tblcfg: tblcfg['outFile'] = True
    if tblcfg['outFile']:
        if 'outFileName' not in tblcfg: tblcfg['outFileName'] = createOutFileName(tblcfg['outColumnNames'], tblcfg['indices'])
        if 'outFilePath' not in tblcfg: tblcfg['outFilePath'] = os.path.join(outDir, tblcfg['outFileName'])
    return tblcfg

##__________________________________________________________________||
def createOutFileName(columnNames, indices, prefix = 'tbl_component_', suffix = '.txt'):
    # for example, if columnNames = ('var1', 'var2', 'var3') and indices = (1, None, 2),
    # l will be ['var1', '1', 'var2', 'var3', '2']
    l = columnNames if indices is None else [str(e) for sublist in zip(columnNames, indices) for e in sublist if e is not None]
    ret = prefix + '_'.join(l) + suffix # e.g. "tbl_component_var1_1_var2_var3_2.txt"
    return ret

##__________________________________________________________________||
def createEventReaderCollectorAssociator(tblcfg):
    keyComposerFactory = GenericKeyComposerBFactory(tblcfg['branchNames'], tblcfg['binnings'], tblcfg['indices'])
    counterFactory = CounterFactory(
        countMethodClass = tblcfg['countsClass'],
        keyComposerFactory = keyComposerFactory,
        binnings = tblcfg['binnings']
    )
    resultsCombinationMethod = CombineIntoList(keyNames = tblcfg['outColumnNames'])
    deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return EventReaderCollectorAssociator(counterFactory, collector)

##__________________________________________________________________||
def buildEventLoopRunner(progressMonitor, communicationChannel, processes):
    if communicationChannel is None: # single process
        eventLoopRunner = EventLoopRunner(progressMonitor)
    else:
        eventLoopRunner = MPEventLoopRunner(communicationChannel)
    return eventLoopRunner

##__________________________________________________________________||
def createEventReaderBundle(eventBuilder, eventSelection, eventReaderCollectorAssociators, progressMonitor, communicationChannel, processes, quiet):
    eventReaderCollectorAssociatorComposite = EventReaderCollectorAssociatorComposite(progressMonitor.createReporter())
    for associator in eventReaderCollectorAssociators: eventReaderCollectorAssociatorComposite.add(associator)
    eventLoopRunner = buildEventLoopRunner(progressMonitor = progressMonitor, communicationChannel = communicationChannel, processes = processes)
    eventReaderBundle = EventReaderBundle(eventBuilder, eventLoopRunner, eventReaderCollectorAssociatorComposite, eventSelection = eventSelection)
    return eventReaderBundle

##__________________________________________________________________||
def createTreeReader(args, progressMonitor, communicationChannel, analyzerName, fileName, treeName, tableConfigs, eventSelection):
    tableConfigs = [completeTableConfig(c, args.outDir) for c in tableConfigs]
    if not args.force: tableConfigs = [c for c in tableConfigs if c['outFile'] and not os.path.exists(c['outFilePath'])]
    eventReaderCollectorAssociators = [createEventReaderCollectorAssociator(c) for c in tableConfigs]
    eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)
    eventReaderBundle = createEventReaderBundle(eventBuilder, eventSelection, eventReaderCollectorAssociators, progressMonitor, communicationChannel, args.processes, args.quiet)
    return eventReaderBundle

##__________________________________________________________________||
class AlphaTwirl(object):

    def __init__(self):
        self.args = None
        self.componentReaders = ComponentReaderComposite()
        self.are_CommunicationChannel_and_ProgressMonitor_created = False

    def ArgumentParser(self, *args, **kwargs):
        parser = ArgumentParser(self, *args, **kwargs)
        parser = self._add_arguments(parser)
        return parser

    def _add_arguments(self, parser):
        parser.add_argument('-i', '--heppydir', default = '/Users/sakuma/work/cms/c150130_RA1_data/PHYS14/20150507_SingleMu', action = 'store', help = "Heppy results dir")
        parser.add_argument("-p", "--processes", action = "store", default = None, type = int, help = "number of processes to run in parallel")
        parser.add_argument("-q", "--quiet", action = "store_true", default = False, help = "quiet mode")
        parser.add_argument('-o', '--outDir', default = 'tbl/out', action = 'store')
        parser.add_argument("-n", "--nevents", action = "store", default = -1, type = int, help = "maximum number of events to process for each component")
        parser.add_argument("--force", action = "store_true", default = False, dest="force", help = "recreate all output files")
        return parser

    def _create_CommunicationChannel_and_ProgressMonitor(self):
        if self.are_CommunicationChannel_and_ProgressMonitor_created: return
        self.progressBar = None if self.args.quiet else ProgressBar()
        if self.args.processes is None:
            self.progressMonitor = NullProgressMonitor() if self.args.quiet else ProgressMonitor(presentation = self.progressBar)
            self.communicationChannel = None
        else:
            self.progressMonitor = NullProgressMonitor() if self.args.quiet else BProgressMonitor(presentation = self.progressBar)
            self.communicationChannel = CommunicationChannel(self.args.processes, self.progressMonitor)
        self.are_CommunicationChannel_and_ProgressMonitor_created = True

    def addComponentReader(self, reader):
        self.componentReaders.add(reader)

    def addTreeReader(self, **kargs):
        if self.args is None: self.ArgumentParser().parse_args()
        self._create_CommunicationChannel_and_ProgressMonitor()
        treeReader = createTreeReader(self.args, self.progressMonitor, self.communicationChannel, **kargs)
        self.addComponentReader(treeReader)

    def run(self):
        if self.args is None: self.ArgumentParser().parse_args()
        self._create_CommunicationChannel_and_ProgressMonitor()
        if self.progressMonitor is not None: self.progressMonitor.begin()
        if self.communicationChannel is not None: self.communicationChannel.begin()
        componentLoop = ComponentLoop(self.componentReaders)
        heppyResult = HeppyResult(self.args.heppydir)
        componentLoop(heppyResult.components())
        if self.communicationChannel is not None: self.communicationChannel.end()
        if self.progressMonitor is not None: self.progressMonitor.end()

##__________________________________________________________________||
