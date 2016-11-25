# Tai Sakuma <tai.sakuma@cern.ch>

from .splitfuncs import *

##__________________________________________________________________||
class DatasetIntoEventBuildersSplitter(object):

    def __init__(self, EventBuilder, eventBuilderConfigMaker, maxEvents = -1, maxEventsPerRun = -1):

        if maxEventsPerRun == 0:
            raise ValueError("maxEventsPerRun cannot be 0")

        self.EventBuilder = EventBuilder
        self.eventBuilderConfigMaker = eventBuilderConfigMaker
        self.maxEvents = maxEvents
        self.maxEventsPerRun = maxEventsPerRun

    def __call__(self, dataset):
        configs = self._split_into_configs(dataset)
        eventBuilders = [self.EventBuilder(c) for c in configs]
        return eventBuilders

    def _split_into_configs(self, dataset):
        file_start_length_list = self._file_start_length_list(dataset)
        configs = [ ]
        for file_, start, length in file_start_length_list:
            config = self.eventBuilderConfigMaker.create_config_for(dataset, file_, start, length)
            configs.append(config)
        return configs

    def _file_start_length_list(self, dataset):

        if self.maxEventsPerRun < 0 and self.maxEvents < 0:
            files = self.eventBuilderConfigMaker.file_list_in(dataset)
            return [(file_, 0, -1) for file_ in files]

        file_nevents_list = self.eventBuilderConfigMaker.file_nevents_list_for(dataset)
        file_start_length_list = create_file_start_length_list(file_nevents_list, self.maxEventsPerRun, self.maxEvents)
        return file_start_length_list
##__________________________________________________________________||
