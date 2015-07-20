# Tai Sakuma <tai.sakuma@cern.ch>
import argparse
import sys
import os
import itertools

from Configure import TableConfigCompleter
from Configure import EventReaderCollectorAssociatorBuilder
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
def buildEventLoopRunner(progressMonitor, communicationChannel, processes):
    if communicationChannel is None: # single process
        eventLoopRunner = EventLoopRunner(progressMonitor)
    else:
        eventLoopRunner = MPEventLoopRunner(communicationChannel)
    return eventLoopRunner

##__________________________________________________________________||
def createTreeReader(progressMonitor, communicationChannel, outDir, force, nevents, processes, analyzerName, fileName, treeName, tableConfigs, eventSelection):
    tableConfigCompleter = TableConfigCompleter(defaultCountsClass = Counts, defaultOutDir = outDir)
    tableConfigs = [tableConfigCompleter.complete(c) for c in tableConfigs]
    if not force: tableConfigs = [c for c in tableConfigs if c['outFile'] and not os.path.exists(c['outFilePath'])]

    tableCreatorBuilder = EventReaderCollectorAssociatorBuilder()
    tableCreators = EventReaderCollectorAssociatorComposite(progressMonitor.createReporter())
    for tblcfg in tableConfigs:
        tableCreators.add(tableCreatorBuilder.build(tblcfg))

    eventLoopRunner = buildEventLoopRunner(progressMonitor = progressMonitor, communicationChannel = communicationChannel, processes = processes)

    eventBuilder = EventBuilder(analyzerName, fileName, treeName, nevents)
    eventReaderBundle = EventReaderBundle(eventBuilder, eventLoopRunner, tableCreators, eventSelection = eventSelection)

    return eventReaderBundle

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

    def _create_CommunicationChannel_and_ProgressMonitor(self):
        self.progressBar = None if self.args.quiet else ProgressBar()
        if self.args.processes is None:
            self.progressMonitor = NullProgressMonitor() if self.args.quiet else ProgressMonitor(presentation = self.progressBar)
            self.communicationChannel = None
        else:
            self.progressMonitor = NullProgressMonitor() if self.args.quiet else BProgressMonitor(presentation = self.progressBar)
            self.communicationChannel = CommunicationChannel(self.args.processes, self.progressMonitor)

    def addComponentReader(self, reader):
        self.componentReaders.add(reader)

    def addTreeReader(self, analyzerName, fileName, treeName,
                      tableConfigs, eventSelection = None):
        cfg = dict(
            analyzerName = analyzerName,
            fileName = fileName,
            treeName = treeName,
            tableConfigs = tableConfigs,
            eventSelection = eventSelection
            )

        self.treeReaderConfigs.append(cfg)

    def run(self):
        if self.args is None: self.ArgumentParser().parse_args()
        self._create_CommunicationChannel_and_ProgressMonitor()
        for cfg in self.treeReaderConfigs:
            treeReader = createTreeReader(
                self.progressMonitor,
                self.communicationChannel,
                self.args.outDir,
                self.args.force,
                self.args.nevents,
                self.args.processes,
                **cfg)
            self.addComponentReader(treeReader)
        if self.progressMonitor is not None: self.progressMonitor.begin()
        if self.communicationChannel is not None: self.communicationChannel.begin()
        componentLoop = ComponentLoop(self.componentReaders)
        if self.args.components == ['all']: self.args.components = None
        heppyResult = HeppyResult(path = self.args.heppydir, componentNames = self.args.components)
        componentLoop(heppyResult.components())
        if self.communicationChannel is not None: self.communicationChannel.end()
        if self.progressMonitor is not None: self.progressMonitor.end()

##__________________________________________________________________||
