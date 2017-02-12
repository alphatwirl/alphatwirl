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

    def file_list_in(self, dataset, maxFiles = -1):
        component = dataset
        files = [os.path.join(getattr(component, self.analyzerName).path, self.fileName)]
        if maxFiles < 0:
            return files
        return files[:min(maxFiles, len(files))]

    def file_nevents_list_for(self, dataset, maxEvents = -1, maxFiles = -1):
        files = self.file_list_in(dataset, maxFiles = maxFiles)
        totalEvents = 0
        ret = [ ]
        for f in files:
            if 0 <= maxEvents <= totalEvents:
                return ret
            n = self.nevents_in_file(f)
            ret.append((f, n))
            totalEvents += n
        return ret

    def nevents_in_file(self, path):
        file = ROOT.TFile.Open(path)
        tree = file.Get(self.treeName)
        return tree.GetEntries()
##__________________________________________________________________||
