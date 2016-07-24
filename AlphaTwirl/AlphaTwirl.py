# Tai Sakuma <tai.sakuma@cern.ch>
import argparse
import sys
import os

from .HeppyResult import ComponentReaderComposite
from .HeppyResult import ComponentLoop
from .HeppyResult import HeppyResult
from .CombineIntoList import CombineIntoList
from .WriteListToFile import WriteListToFile
from .Configure import build_progressMonitor_communicationChannel

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
