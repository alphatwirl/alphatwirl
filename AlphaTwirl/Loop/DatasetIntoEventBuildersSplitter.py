# Tai Sakuma <tai.sakuma@cern.ch>

from .splitfuncs import create_file_start_length_list

##__________________________________________________________________||
class DatasetIntoEventBuildersSplitter(object):

    def __init__(self, EventBuilder, eventBuilderConfigMaker,
                 maxEvents = -1, maxEventsPerRun = -1, maxFiles = -1
    ):

        if maxEventsPerRun == 0:
            raise ValueError("maxEventsPerRun cannot be 0")

        self.EventBuilder = EventBuilder
        self.eventBuilderConfigMaker = eventBuilderConfigMaker
        self.maxEvents = maxEvents
        self.maxEventsPerRun = maxEventsPerRun
        self.maxFiles = maxFiles

    def __repr__(self):
        return '{}(EventBuilder = {!r}, eventBuilderConfigMaker = {!r}, maxEvents = {!r}, maxEventsPerRun = {!r}'.format(
            self.__class__.__name__,
            self.EventBuilder,
            self.eventBuilderConfigMaker,
            self.maxEvents,
            self.maxEventsPerRun
        )

    def __call__(self, dataset):
        file_start_length_list = self._file_start_length_list(dataset)
        configs = self._create_configs(dataset, file_start_length_list)
        eventBuilders = [self.EventBuilder(c) for c in configs]
        return eventBuilders

    def _file_start_length_list(self, dataset):

        if self.maxEventsPerRun < 0 and self.maxEvents < 0:
            files = self.eventBuilderConfigMaker.file_list_in(dataset, maxFiles = self.maxFiles)
            return [(file_, 0, -1) for file_ in files]

        file_nevents_list = self.eventBuilderConfigMaker.file_nevents_list_for(
            dataset,
            maxEvents = self.maxEvents,
            maxFiles = self.maxFiles
        )
        file_start_length_list = create_file_start_length_list(file_nevents_list, self.maxEventsPerRun, self.maxEvents)
        return file_start_length_list

    def _create_configs(self, dataset, file_start_length_list):
        configs = [ ]
        for file_, start, length in file_start_length_list:
            config = self.eventBuilderConfigMaker.create_config_for(dataset, file_, start, length)
            configs.append(config)
        return configs
##__________________________________________________________________||
