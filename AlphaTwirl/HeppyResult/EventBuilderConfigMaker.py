# Tai Sakuma <tai.sakuma@cern.ch>
import os

import ROOT

from .EventBuilderConfig import EventBuilderConfig

##__________________________________________________________________||
class EventBuilderConfigMaker(object):
    def __init__(self, analyzerName, fileName, treeName):

        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName

    def create_config_for(self, dataset, file_, start, length):
        config = EventBuilderConfig(
            inputPath = file_,
            treeName = self.treeName,
            maxEvents = length,
            start = start,
            component = dataset, # for scribblers
            name = dataset.name # for the progress report writer
        )
        return config

    def file_list_in(self, dataset):
        component = dataset
        input_path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        return [input_path]

    def file_nevents_list_for(self, dataset):
        component = dataset
        input_path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        ntotal = self.nevents_in_file(input_path)
        return [(input_path, ntotal)]

    def nevents_in_file(self, path):
        file = ROOT.TFile.Open(path)
        tree = file.Get(self.treeName)
        return tree.GetEntries()
##__________________________________________________________________||
