# Tai Sakuma <tai.sakuma@cern.ch>
import argparse
import sys
import os, errno
import itertools

from HeppyResult.HeppyResultReader import HeppyResultReader
from HeppyResult.HeppyResult import HeppyResult
from EventReader.EventReaderBundle import EventReaderBundle
from EventReader.EventReaderPackage import EventReaderPackage
from EventReader.EventLoopRunner import EventLoopRunner
from EventReader.MPEventLoopRunner import MPEventLoopRunner
from ProgressBar.ProgressBar import ProgressBar
from ProgressBar.ProgressMonitor import ProgressMonitor, MPProgressMonitor
from Counter.CountsWithEmptyNextKeys import CountsWithEmptyNextKeysFactory
from Counter.Counts import Counts
from Counter.GenericKeyComposer import GenericKeyComposer
from Counter.GenericKeyComposerB import GenericKeyComposerBFactory
from Counter.CounterFactory import CounterFactory
from CombineIntoList import CombineIntoList
from WriteListToFile import WriteListToFile
from EventReader.Collector import Collector

try:
    from HeppyResult.BEventBuilder import BEventBuilder as EventBuilder
except ImportError:
    pass

##____________________________________________________________________________||
def mkdir_p(path):
    # http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

##____________________________________________________________________________||
class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, owner, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.owner = owner

    def parse_args(self, *args, **kwargs):
        args = super(ArgumentParser, self).parse_args(*args, **kwargs)
        self.owner.args = args
        return args

##____________________________________________________________________________||
defaultCountsBuilderClass = CountsWithEmptyNextKeysFactory(Counts)

##____________________________________________________________________________||
def completeTableConfig(tblcfg, outDir):
    if 'outColumnNames' not in tblcfg: tblcfg['outColumnNames'] = tblcfg['branchNames']
    if 'indices' not in tblcfg: tblcfg['indices'] = None
    if 'outFileName' not in tblcfg: tblcfg['outFileName'] = createOutFileName(tblcfg['outColumnNames'], tblcfg['indices'])
    if 'countsClass' not in tblcfg: tblcfg['countsClass'] = defaultCountsBuilderClass
    if 'outFilePath' not in tblcfg: tblcfg['outFilePath'] = os.path.join(outDir, tblcfg['outFileName'])
    return tblcfg

##____________________________________________________________________________||
def createOutFileName(columnNames, indices, prefix = 'tbl_component_', suffix = '.txt'):
    # for example, if columnNames = ('var1', 'var2', 'var3') and indices = (1, None, 2),
    # l will be ['var1', '1', 'var2', 'var3', '2']
    l = columnNames if indices is None else [str(e) for sublist in zip(columnNames, indices) for e in sublist if e is not None]
    ret = prefix + '_'.join(l) + suffix # e.g. "tbl_component_var1_1_var2_var3_2.txt"
    return ret

##____________________________________________________________________________||
def createPackageFor(tblcfg):
    keyComposer = GenericKeyComposerBFactory(tblcfg['branchNames'], tblcfg['binnings'], tblcfg['indices'])
    counterFactory = CounterFactory(tblcfg['countsClass'], tblcfg['outColumnNames'], keyComposer, tblcfg['binnings'])
    resultsCombinationMethod = CombineIntoList()
    deliveryMethod = WriteListToFile(tblcfg['outFilePath'])
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return EventReaderPackage(counterFactory, collector)

##____________________________________________________________________________||
def buildEventLoopRunner(progressBar, processes, quiet):
    if processes is None:
        progressMonitor = None if quiet else ProgressMonitor(presentation = progressBar)
        eventLoopRunner = EventLoopRunner(progressMonitor)
    else:
        progressMonitor = None if quiet else MPProgressMonitor(presentation = progressBar)
        eventLoopRunner = MPEventLoopRunner(processes, progressMonitor)
    return eventLoopRunner

##____________________________________________________________________________||
def createEventReaderBundle(eventBuilder, eventSelection, eventReaderPackages, processes, quiet):
    progressBar = None if quiet else ProgressBar()
    eventLoopRunner = buildEventLoopRunner(progressBar = progressBar, processes = processes, quiet = quiet)
    eventReaderBundle = EventReaderBundle(eventBuilder, eventLoopRunner, eventSelection = eventSelection, progressBar = progressBar)
    for package in eventReaderPackages:
        eventReaderBundle.addReaderPackage(package)
    return eventReaderBundle

##____________________________________________________________________________||
def createTreeReader(args, analyzerName, fileName, treeName, tableConfigs, eventSelection):
    tableConfigs = [completeTableConfig(c, args.outDir) for c in tableConfigs]
    if not args.force: tableConfigs = [c for c in tableConfigs if not os.path.exists(c['outFilePath'])]
    eventReaderPackages = [createPackageFor(c) for c in tableConfigs]
    eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)
    eventReaderBundle = createEventReaderBundle(eventBuilder, eventSelection, eventReaderPackages, args.processes, args.quiet)
    return eventReaderBundle

##____________________________________________________________________________||
class AlphaTwirl(object):

    def __init__(self):
        self.args = None
        self.componentReaders = [ ]

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
        self.componentReaders.append(reader)

    def addTreeReader(self, **kargs):
        if self.args is None: self.ArgumentParser().parse_args()
        treeReader = createTreeReader(self.args, **kargs)
        self.addComponentReader(treeReader)

    def run(self):
        if self.args is None: self.ArgumentParser().parse_args()
        mkdir_p(self.args.outDir)
        heppyResultReader = self._buildHeppyResultReader()
        heppyResult = HeppyResult(self.args.heppydir)
        heppyResultReader.read(heppyResult)

    def _buildHeppyResultReader(self):
        heppyResultReader = HeppyResultReader()
        while len(self.componentReaders) > 0: heppyResultReader.addReader(self.componentReaders.pop(0))
        return heppyResultReader

##____________________________________________________________________________||
