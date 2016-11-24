# Tai Sakuma <tai.sakuma@cern.ch>

import os
import collections

import ROOT

from .Chunk import Chunk
from .splitfuncs import *

##__________________________________________________________________||
class ComponentSplitter(object):
    """Split a component into chunks
    """
    def __init__(self, analyzerName, fileName, treeName,
                 maxEvents = -1, maxEventsPerRun = -1):

        if maxEventsPerRun == 0:
            raise ValueError("maxEventsPerRun cannot be 0")

        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName
        self.maxEvents = maxEvents
        self.maxEventsPerRun = maxEventsPerRun

    def split(self, component):
        file_start_length_list = self._file_start_length_list(component)
        chunks = [ ]
        for file, start, length in file_start_length_list:
            chunk = Chunk(
                inputPath = file,
                treeName = self.treeName,
                maxEvents = length,
                start = start,
                component = component, # for scribblers
                name = component.name # for the progress report writer
            )
            chunks.append(chunk)
        return chunks

    def _file_start_length_list(self, component):

        if self.maxEventsPerRun < 0:
            inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
            return [(inputPath, 0, -1)]

        file_nevents_list = self._file_nevents_list(component)
        file_start_length_list = create_file_start_length_list(file_nevents_list, self.maxEventsPerRun, self.maxEvents)
        return file_start_length_list

    def _file_nevents_list(self, component):
        input_path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        nTotal = self._nevents_in_file(input_path)
        return [(input_path, nTotal)]

    def _nevents_in_file(self, path):
        file = ROOT.TFile.Open(path)
        tree = file.Get(self.treeName)
        return tree.GetEntries()

##__________________________________________________________________||
