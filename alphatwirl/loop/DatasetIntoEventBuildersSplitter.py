# Tai Sakuma <tai.sakuma@cern.ch>

from .splitfuncs import create_file_start_length_list

##__________________________________________________________________||
class DatasetIntoEventBuildersSplitter(object):

    def __init__(self, EventBuilder, eventBuilderConfigMaker,
                 maxEvents = -1, maxEventsPerRun = -1,
                 maxFiles = -1, maxFilesPerRun = 1
    ):

        self.EventBuilder = EventBuilder
        self.eventBuilderConfigMaker = eventBuilderConfigMaker
        self.maxEvents = maxEvents
        self.maxEventsPerRun = maxEventsPerRun
        self.maxFiles = maxFiles
        self.maxFilesPerRun = maxFilesPerRun
        self.create_file_start_length_list = create_file_start_length_list

    def __repr__(self):
        return '{}(EventBuilder = {!r}, eventBuilderConfigMaker = {!r}, maxEvents = {!r}, maxEventsPerRun = {!r}, maxFiles = {!r}, maxFilesPerRun = {!r})'.format(
            self.__class__.__name__,
            self.EventBuilder,
            self.eventBuilderConfigMaker,
            self.maxEvents,
            self.maxEventsPerRun,
            self.maxFiles,
            self.maxFilesPerRun
        )

    def __call__(self, dataset):
        file_start_length_list = self._file_start_length_list(
            dataset,
            maxEvents = self.maxEvents,
            maxEventsPerRun = self.maxEventsPerRun,
            maxFiles = self.maxFiles,
            maxFilesPerRun = self.maxFilesPerRun
        )
        configs = self._create_configs(dataset, file_start_length_list)
        eventBuilders = [self.EventBuilder(c) for c in configs]
        return eventBuilders

    def _file_start_length_list(self, dataset, maxEvents = -1, maxEventsPerRun = -1,
                                maxFiles = -1, maxFilesPerRun = 1):

        if maxEvents < 0 and maxEventsPerRun < 0:
            # fast path. unnecessary to get the number events in the files
            files = self.eventBuilderConfigMaker.file_list_in(dataset, maxFiles = maxFiles)
            if not files:
                return [ ]
            if maxFilesPerRun < 0:
                return [(files, 0, -1)]
            if maxFilesPerRun == 0:
                return [ ]
            return [(files[i:(i + maxFilesPerRun)], 0, -1) for i in range(0, len(files), maxFilesPerRun)]

        # this can be slow
        file_nevents_list = self._file_nevents_list_for(
            dataset,
            maxEvents = maxEvents,
            maxFiles = maxFiles
        )


        file_start_length_list = self.create_file_start_length_list(
            file_nevents_list = file_nevents_list,
            max_events_per_run = maxEventsPerRun,
            max_events_total = maxEvents,
            max_files_per_run = maxFilesPerRun
        )
        return file_start_length_list

    def _file_nevents_list_for(self, dataset, maxEvents = -1, maxFiles = -1):
        files = self.eventBuilderConfigMaker.file_list_in(dataset, maxFiles = maxFiles)
        totalEvents = 0
        ret = [ ]
        for f in files:
            if 0 <= maxEvents <= totalEvents:
                return ret
            n = self.eventBuilderConfigMaker.nevents_in_file(f)
            ret.append((f, n))
            totalEvents += n
        return ret

    def _create_configs(self, dataset, file_start_length_list):
        configs = [ ]
        for files, start, length in file_start_length_list:
            config = self.eventBuilderConfigMaker.create_config_for(dataset, files, start, length)
            configs.append(config)
        return configs
##__________________________________________________________________||
