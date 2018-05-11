# Tai Sakuma <tai.sakuma@gmail.com>
import os
import logging

import ROOT

from .EventBuilderConfig import EventBuilderConfig
from .load_delphes import load_delphes

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='alphatwirl.delphes has been moved to https://github.com/alphatwirl/atdelphes.')
class EventBuilderConfigMaker(object):
    def __init__(self):
        self.treeName = 'Delphes'

    def create_config_for(self, dataset, files, start, length):
        config = EventBuilderConfig(
            inputPaths = files,
            treeName = self.treeName,
            maxEvents = length,
            start = start,
            dataset = dataset, # for scribblers
            name = dataset.name # for the progress report writer
        )
        return config

    def file_list_in(self, dataset, maxFiles):
        if maxFiles < 0:
            return dataset.files
        return dataset.files[:min(maxFiles, len(dataset.files))]

    def nevents_in_file(self, path):
        load_delphes()
        try:
            file = ROOT.TFile.Open(path)
            tree = file.Get(self.treeName)
            return tree.GetEntriesFast()

        except StandardError as e:
            logger = logging.getLogger(__name__)
            logger.warning(str(e))
            logger.warning(path)
            logger.warning('returning 0')
            return 0

##__________________________________________________________________||
