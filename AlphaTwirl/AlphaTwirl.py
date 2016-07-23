# Tai Sakuma <tai.sakuma@cern.ch>
import argparse
import sys
import os

from .HeppyResult import ComponentReaderComposite
from .HeppyResult import ComponentLoop
from .HeppyResult import HeppyResult
from .EventReader import Collector
from .EventReader import NullCollector
from .EventReader import CollectorComposite
from .EventReader import CollectorDelegate
from .Concurrently import CommunicationChannel
from .Concurrently import CommunicationChannel0
from .ProgressBar import ProgressBar
from .ProgressBar import ProgressPrint
from .ProgressBar import ProgressMonitor, BProgressMonitor, NullProgressMonitor
from .Counter import Counter, GenericKeyComposerB, NextKeyComposer
from .CombineIntoList import CombineIntoList
from .WriteListToFile import WriteListToFile

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
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return counter, collector

##__________________________________________________________________||
config_default = dict(
    heppydir = '/Users/sakuma/work/cms/c150130_RA1_data/80X/MC/20160708_B01_MCMiniAODv2_SM/AtLogic_MCMiniAODv2_SM',
    processes = None,
    quiet = False,
    components = None,
)

##__________________________________________________________________||
class AlphaTwirlConfigurerFromArgs():

    def __init__(self):
        self.cfg = config_default.copy()

    def add_arguments(self, parser):
        parser.add_argument('-i', '--heppydir', default = self.cfg['heppydir'], help = 'Heppy results dir')
        parser.add_argument('-p', '--processes', default = self.cfg['processes'], type = int, help = 'number of processes to run in parallel')
        parser.add_argument('-q', '--quiet', action = 'store_true', default = self.cfg['quiet'], help = 'quiet mode')
        parser.add_argument('-c', '--components', default = None, nargs = '*', help = 'the list of components')

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
