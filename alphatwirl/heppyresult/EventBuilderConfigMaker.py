# Tai Sakuma <tai.sakuma@gmail.com>
import os

import ROOT

from .EventBuilderConfig import EventBuilderConfig as HeppyEventBuilderConfig

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class EventBuilderConfigMaker(object):
    def __init__(self, analyzerName, fileName, treeName):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName

    def __repr__(self):
        name_value_pairs = (
            ('analyzerName', self.analyzerName),
            ('fileName', self.fileName),
            ('treeName', self.treeName)
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def create_config_for(self, dataset, files, start, length):
        config = HeppyEventBuilderConfig(
            inputPaths = files,
            treeName = self.treeName,
            maxEvents = length,
            start = start,
            name = dataset.name, # for the progress report writer
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
