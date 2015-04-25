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
from Counter.CountsWithEmptyNextKeys import CountsWithEmptyNextKeysBuilder
from Counter.Counts import Counts
from Counter.KeyComposer import GenericKeyComposer
from Counter.Counter import CounterBuilder
from CombineIntoList import CombineIntoList
from WriteListToFile import WriteListToFile
from EventReader.Collector import Collector

try:
    from HeppyResult.EventBuilder import EventBuilder
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
defaultCountsBuilderClass = CountsWithEmptyNextKeysBuilder(Counts)

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
class AlphaTwirl(object):

    def __init__(self):
        self.args = None
        self.componentReaders = [ ]

    def ArgumentParser(self, *args, **kwargs):
        parser = ArgumentParser(self, *args, **kwargs)
        parser = self._add_arguments(parser)
        return parser

    def _add_arguments(self, parser):
        parser.add_argument('-i', '--heppydir', default = '/Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/201525_SingleMu', action = 'store', help = "Heppy results dir")
        parser.add_argument("-p", "--processes", action = "store", default = None, type = int, help = "number of processes to run in parallel")
        parser.add_argument("-q", "--quiet", action = "store_true", default = False, help = "quiet mode")
        parser.add_argument('-o', '--outDir', default = 'tbl/out', action = 'store')
        parser.add_argument("-n", "--nevents", action = "store", default = -1, type = int, help = "maximum number of events to process for each component")
        parser.add_argument("--force", action = "store_true", default = False, dest="force", help = "recreate all output files")
        return parser

    def addComponentReader(self, reader):
        self.componentReaders.append(reader)

    def addTreeReader(self, analyzerName, fileName, treeName, tableConfigs, eventSelection):
        if self.args is None: self.ArgumentParser().parse_args()
        tableConfigs = [completeTableConfig(c, self.args.outDir) for c in tableConfigs]
        if not self.args.force: tableConfigs = [c for c in tableConfigs if not os.path.exists(c['outFilePath'])]
        eventReaderPackages = [self.createPackageFor(c) for c in tableConfigs]
        branches = set(itertools.chain(*[list(cfg['branchNames']) for cfg in tableConfigs]))
        eventBuilder = EventBuilder(analyzerName, fileName, treeName, self.args.nevents, branches)
        eventReaderBundle = self.createEventReaderBundle(eventBuilder, eventSelection, eventReaderPackages)
        self.addComponentReader(eventReaderBundle)

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

    def buildEventLoopRunner(self, progressBar):
        if self.args.processes is None:
            progressMonitor = None if self.args.quiet else ProgressMonitor(presentation = progressBar)
            eventLoopRunner = EventLoopRunner(progressMonitor)
        else:
            progressMonitor = None if self.args.quiet else MPProgressMonitor(presentation = progressBar)
            eventLoopRunner = MPEventLoopRunner(self.args.processes, progressMonitor)
        return eventLoopRunner

    def createEventReaderBundle(self, eventBuilder, eventSelection, eventReaderPackages):
        progressBar = None if self.args.quiet else ProgressBar()
        eventLoopRunner = self.buildEventLoopRunner(progressBar = progressBar)
        eventReaderBundle = EventReaderBundle(eventBuilder, eventLoopRunner, eventSelection = eventSelection, progressBar = progressBar)
        for package in eventReaderPackages:
            eventReaderBundle.addReaderPackage(package)
        return eventReaderBundle

    def createPackageFor(self, tblcfg):
        keyComposer = GenericKeyComposer(tblcfg['branchNames'], tblcfg['binnings'], tblcfg['indices'])
        counterBuilder = CounterBuilder(tblcfg['countsClass'], tblcfg['outColumnNames'], keyComposer)
        resultsCombinationMethod = CombineIntoList()
        deliveryMethod = WriteListToFile(tblcfg['outFilePath'])
        collector = Collector(resultsCombinationMethod, deliveryMethod)
        return EventReaderPackage(counterBuilder, collector)

##____________________________________________________________________________||
