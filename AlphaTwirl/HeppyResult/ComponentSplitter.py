# Tai Sakuma <tai.sakuma@cern.ch>

import os
import collections

import ROOT

from .Chunk import Chunk

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
        if self.maxEventsPerRun < 0:
            return self._one_chunk_for_the_component(component)
        return self._split_the_component_into_multiple_chunks(component)

    def _one_chunk_for_the_component(self, component):
        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        chunk = Chunk(
            inputPath = inputPath,
            treeName = self.treeName,
            maxEvents = self.maxEvents,
            start = 0,
            component = component, # for scribblers
            name = component.name # for the progress report writer
        )
        return [chunk]

    def _split_the_component_into_multiple_chunks(self, component):
        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        nTotal = self._get_number_of_events_in_component(component)
        nTotal =  self._minimum_positive_value([self.maxEvents, nTotal])
        chunks = [ ]
        for start, nEvents in self._create_start_nEvents_list(nTotal, self.maxEventsPerRun):
            chunk = Chunk(
                inputPath = inputPath,
                treeName = self.treeName,
                maxEvents = nEvents,
                start = start,
                component = component, # for scribblers
                name = component.name # for the progress report writer
            )
            chunks.append(chunk)
        return chunks

    def _get_number_of_events_in_component(self, component):
        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self.treeName)
        return tree.GetEntries()

    def _create_start_nEvents_list(self, nTotal, nPerRun):
        nLoops = nTotal/nPerRun
        ret = [(i*nPerRun, nPerRun) for i in range(nLoops)]
        if nTotal % nPerRun > 0:
            ret.append((nLoops*nPerRun, nTotal % nPerRun))
        return ret

    def _minimum_positive_value(self, vals):
        vals = [v for v in vals if v >= 0]
        if not vals: return -1
        return min(vals)
##__________________________________________________________________||
