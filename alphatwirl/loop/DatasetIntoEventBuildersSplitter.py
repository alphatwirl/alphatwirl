# Tai Sakuma <tai.sakuma@gmail.com>

from .splitfuncs import create_files_start_length_list

##__________________________________________________________________||
class DatasetIntoEventBuildersSplitter(object):

    def __init__(self, EventBuilder, eventBuilderConfigMaker,
                 maxEvents=-1, maxEventsPerRun=-1,
                 maxFiles=-1, maxFilesPerRun=1
    ):

        self.EventBuilder = EventBuilder
        self.eventBuilderConfigMaker = eventBuilderConfigMaker
        self.max_events = maxEvents
        self.max_events_per_run = maxEventsPerRun
        self.max_files = maxFiles
        self.max_files_per_run = maxFilesPerRun

    def __repr__(self):
        return '{}(EventBuilder={!r}, eventBuilderConfigMaker={!r}, maxEvents={!r}, maxEventsPerRun={!r}, maxFiles={!r}, maxFilesPerRun={!r})'.format(
            self.__class__.__name__,
            self.EventBuilder,
            self.eventBuilderConfigMaker,
            self.max_events,
            self.max_events_per_run,
            self.max_files,
            self.max_files_per_run
        )

    def __call__(self, dataset):

        files = self.eventBuilderConfigMaker.file_list_in(dataset, maxFiles=self.max_files)
        # e.g., ['A.root', 'B.root', 'C.root', 'D.root', 'E.root']

        files_start_length_list = create_files_start_length_list(
            files,
            func_get_nevents_in_file=self.eventBuilderConfigMaker.nevents_in_file,
            max_events=self.max_events,
            max_events_per_run=self.max_events_per_run,
            max_files=self.max_files,
            max_files_per_run=self.max_files_per_run
        )
        # (files, start, length)
        # e.g.,
        # [
        #     (['A.root'], 0, 80),
        #     (['A.root', 'B.root'], 80, 80),
        #     (['B.root'], 60, 80),
        #     (['B.root', 'C.root'], 140, 80),
        #     (['C.root'], 20, 10)
        # ]

        configs = self._create_configs(dataset, files_start_length_list)
        eventBuilders = [self.EventBuilder(c) for c in configs]
        return eventBuilders

    def _create_configs(self, dataset, file_start_length_list):
        configs = [ ]
        for files, start, length in file_start_length_list:
            config = self.eventBuilderConfigMaker.create_config_for(dataset, files, start, length)
            configs.append(config)
        return configs
##__________________________________________________________________||
