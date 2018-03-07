# Tai Sakuma <tai.sakuma@gmail.com>

from .splitfuncs import create_file_start_length_list

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
        self.create_file_start_length_list = create_file_start_length_list

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

        files_start_length_list = self._file_start_length_list(
            files,
            max_events=self.max_events,
            max_events_per_run=self.max_events_per_run,
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

    def _file_start_length_list(self, files, max_events, max_events_per_run,
                                max_files_per_run):

        if not self._need_get_number_of_events_in_files(max_events, max_events_per_run):
            return self._fast_path(files, max_files_per_run)

        func_get_nevents_in_file=self.eventBuilderConfigMaker.nevents_in_file
        return self._full_path(files, func_get_nevents_in_file, max_events, max_events_per_run, max_files_per_run)

    def _need_get_number_of_events_in_files(self, max_events, max_events_per_run):
        return max_events >= 0 or max_events_per_run >= 0

    def _fast_path(self, files, max_files_per_run):
        if not files:
            return [ ]
        if max_files_per_run < 0:
            return [(files, 0, -1)]
        if max_files_per_run == 0:
            return [ ]
        return [(files[i:(i + max_files_per_run)], 0, -1) for i in range(0, len(files), max_files_per_run)]

    def _full_path(self, files, func_get_nevents_in_file, max_events, max_events_per_run, max_files_per_run):

        # this can be slow
        file_nevents_list = self._file_nevents_list_(
            files,
            func_get_nevents_in_file=func_get_nevents_in_file,
            max_events=max_events
        )

        file_start_length_list = self.create_file_start_length_list(
            file_nevents_list=file_nevents_list,
            max_events_per_run=max_events_per_run,
            max_events_total=max_events,
            max_files_per_run=max_files_per_run
        )
        return file_start_length_list

    def _file_nevents_list_(self, files, func_get_nevents_in_file, max_events):
        total_events = 0
        ret = [ ]
        for f in files:
            if 0 <= max_events <= total_events:
                break

            # this can be slow
            n = func_get_nevents_in_file(f)

            ret.append((f, n))
            total_events += n
        return ret

    def _create_configs(self, dataset, file_start_length_list):
        configs = [ ]
        for files, start, length in file_start_length_list:
            config = self.eventBuilderConfigMaker.create_config_for(dataset, files, start, length)
            configs.append(config)
        return configs
##__________________________________________________________________||
