# Tai Sakuma <tai.sakuma@cern.ch>
import os

import ROOT

from ..roottree import EventBuilderConfig as BaseEventBuilderConfig
from .EventBuilderConfig import EventBuilderConfig as HeppyEventBuilderConfig

##__________________________________________________________________||
class EventBuilderConfigMaker(object):
    def __init__(self, analyzerName, fileName, treeName):

        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName

    def create_config_for(self, dataset, files, start, length):
        base_config = BaseEventBuilderConfig(
            inputPaths = files,
            treeName = self.treeName,
            maxEvents = length,
            start = start,
            name = dataset.name # for the progress report writer
        )
        config = HeppyEventBuilderConfig(
            base = base_config,
            component = dataset # for scribblers
        )
        return config

    def file_list_in(self, dataset, maxFiles = -1):
        component = dataset
        files = [os.path.join(getattr(component, self.analyzerName).path, self.fileName)]
        if maxFiles < 0:
            return files
        return files[:min(maxFiles, len(files))]

    def nevents_in_file(self, path):
        file = ROOT.TFile.Open(path)
        tree = file.Get(self.treeName)
        return tree.GetEntries() # GetEntries() is slow. call only as
                                 # many times as necessary

##__________________________________________________________________||
