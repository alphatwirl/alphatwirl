# Tai Sakuma <tai.sakuma@cern.ch>
import argparse
import sys
import os
import itertools

from HeppyResult.ComponentReaderComposite import ComponentReaderComposite
from HeppyResult.ComponentLoop import ComponentLoop
from HeppyResult.HeppyResult import HeppyResult
from EventReader.EventReaderBundle import EventReaderBundle
from EventReader.EventReaderCollectorAssociator import EventReaderCollectorAssociator
from EventReader.EventReaderCollectorAssociatorComposite import EventReaderCollectorAssociatorComposite
from EventReader.EventLoopRunner import EventLoopRunner
from EventReader.MPEventLoopRunner import MPEventLoopRunner
from ProgressBar.ProgressBar import ProgressBar
from ProgressBar.ProgressMonitor import ProgressMonitor, MPProgressMonitor
from Counter.Counts import Counts
from Counter.GenericKeyComposerB import GenericKeyComposerBFactory
from Counter.CounterFactory import CounterFactory
from CombineIntoList import CombineIntoList
from WriteListToFile import WriteListToFile
from EventReader.Collector import Collector

try:
    from HeppyResult.BEventBuilder import BEventBuilder as EventBuilder
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
def buildEventLoopRunner(progressBar, processes, quiet):
    if processes is None:
        progressMonitor = None if quiet else ProgressMonitor(presentation = progressBar)
        eventLoopRunner = EventLoopRunner(progressMonitor)
    else:
        progressMonitor = None if quiet else MPProgressMonitor(presentation = progressBar)
        eventLoopRunner = MPEventLoopRunner(processes, progressMonitor)
    return eventLoopRunner

##__________________________________________________________________||
def createEventReaderBundle(eventBuilder, eventSelection, eventReaderCollectorAssociators, processes, quiet):
    progressBar = None if quiet else ProgressBar()
    eventReaderCollectorAssociatorComposite = EventReaderCollectorAssociatorComposite(progressBar)
    for associator in eventReaderCollectorAssociators: eventReaderCollectorAssociatorComposite.add(associator)
    eventLoopRunner = buildEventLoopRunner(progressBar = progressBar, processes = processes, quiet = quiet)
    eventReaderBundle = EventReaderBundle(eventBuilder, eventLoopRunner, eventReaderCollectorAssociatorComposite, eventSelection = eventSelection)
    return eventReaderBundle

##__________________________________________________________________||
def createTreeReader(args, analyzerName, fileName, treeName, tableConfigs, eventSelection):
    tableConfigs = [completeTableConfig(c, args.outDir) for c in tableConfigs]
    if not args.force: tableConfigs = [c for c in tableConfigs if c['outFile'] and not os.path.exists(c['outFilePath'])]
    eventReaderCollectorAssociators = [createEventReaderCollectorAssociator(c) for c in tableConfigs]
    eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)
    eventReaderBundle = createEventReaderBundle(eventBuilder, eventSelection, eventReaderCollectorAssociators, args.processes, args.quiet)
    return eventReaderBundle

##__________________________________________________________________||
class AlphaTwirl(object):

    def __init__(self):
        self.args = None
        self.componentReaders = ComponentReaderComposite()

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

    def addComponentReader(self, reader):
        self.componentReaders.add(reader)

    def addTreeReader(self, **kargs):
        if self.args is None: self.ArgumentParser().parse_args()
        treeReader = createTreeReader(self.args, **kargs)
        self.addComponentReader(treeReader)

    def run(self):
        if self.args is None: self.ArgumentParser().parse_args()
        componentLoop = ComponentLoop(self.componentReaders)
        heppyResult = HeppyResult(self.args.heppydir)
        componentLoop(heppyResult.components())

##__________________________________________________________________||
