import sys
import collections
import unittest

from alphatwirl.loop import DatasetIntoEventBuildersSplitter

##__________________________________________________________________||
MockEventBuilder = collections.namedtuple('MockEventBuilder', 'config')

MockEventBuilderConfig = collections.namedtuple(
    'MockEventBuilderConfig',
    'dataset file_ start length'
)

##__________________________________________________________________||
class MockDataset(object): pass

##__________________________________________________________________||
class MockSplitFunc(object):
    def __init__(self):
        self.args_call = [ ]
        self.ret = None

    def __call__(self, file_nevents_list, max_events_per_run = -1, max_events_total = -1, max_files_per_run = 1):
        self.args_call.append((file_nevents_list, max_events_per_run, max_events_total, max_files_per_run))
        return self.ret

##__________________________________________________________________||
class MockEventBuilderConfigMaker(object):
    def __init__(self):
        self.args_file_list_in = [ ]
        self.args_create_config_for = [ ]
        self.ret_file_list_in = None
        self.ret_create_config_for = None
        self.ret_nevents_in_file = collections.deque()

    def file_list_in(self, dataset, maxFiles):
        self.args_file_list_in.append((dataset, maxFiles))
        if maxFiles < 0:
            return self.ret_file_list_in
        else:
            return self.ret_file_list_in[:maxFiles]

    def nevents_in_file(self, path):
        return self.ret_nevents_in_file.popleft()

    def create_config_for(self, dataset, file_, start, length):
        self.args_create_config_for.append((dataset, file_, start, length))
        return MockEventBuilderConfig(dataset, file_, start, length)

##__________________________________________________________________||
class TestDatasetIntoEventBuildersSplitter(unittest.TestCase):

    def setUp(self):
        self.configMaker = MockEventBuilderConfigMaker()
        self.configMaker.ret_file_list_in = ['A.root', 'B.root', 'C.root', 'D.root', 'E.root']
        self.configMaker.ret_nevents_in_file.extend([100, 200, 150, 180, 210])

        self.obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            self.configMaker,
            )

        self.split_func = MockSplitFunc()
        self.split_func.ret = [
            (['A.root'], 0, 80), (['A.root', 'B.root'], 80, 80),
            (['B.root'], 60, 80), (['B.root', 'C.root'], 140, 80),
            (['C.root'], 20, 10)
        ]
        self.obj.create_file_start_length_list = self.split_func

    def test_repr(self):
        repr(self.obj)

    def test_file_start_length_list_fast_path_00(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = -1         # < 0
        maxFilesPerRun = -1
        expected = [
            (['A.root', 'B.root', 'C.root', 'D.root', 'E.root'], 0, -1),
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, -1)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_fast_path_01(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = -1         # < 0
        maxFilesPerRun = 1
        expected = [
            (['A.root'], 0, -1),
            (['B.root'], 0, -1),
            (['C.root'], 0, -1),
            (['D.root'], 0, -1),
            (['E.root'], 0, -1)
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, -1)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_fast_path_02(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = -1         # < 0
        maxFilesPerRun = 2    # > 0
        expected = [
            (['A.root', 'B.root'], 0, -1),
            (['C.root', 'D.root'], 0, -1),
            (['E.root'], 0, -1)
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, -1)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_fast_path_03(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = 3          # > 0
        maxFilesPerRun = 2    # > 0
        expected = [
            (['A.root', 'B.root'], 0, -1),
            (['C.root'], 0, -1),
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, 3)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_fast_path_04(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = 0          # = 0
        maxFilesPerRun = 2    # > 0
        expected = [
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, 0)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_fast_path_05(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = 0          # = 0
        maxFilesPerRun = 0    # = 0
        expected = [
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, 0)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_fast_path_05(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = -1         # < 0
        maxFilesPerRun = 0    # = 0
        expected = [
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, -1)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_long_path(self):
        dataset = MockDataset()
        maxEvents = 330        # > 0
        maxEventsPerRun = 80   # > 0
        maxFiles = 4           # > 0
        maxFilesPerRun = 2     # > 0
        expected = [
            (['A.root'], 0, 80), (['A.root', 'B.root'], 80, 80),
            (['B.root'], 60, 80), (['B.root', 'C.root'], 140, 80),
            (['C.root'], 20, 10)
        ]
        actual = self.obj._file_start_length_list(
            dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun,
            maxFiles = maxFiles, maxFilesPerRun = maxFilesPerRun
        )
        self.assertEqual([(dataset, 4)], self.configMaker.args_file_list_in)
        self.assertEqual([([('A.root', 100), ('B.root', 200), ('C.root', 150)], 80, 330, 2)], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_nevents_list_for(self):

        dataset = MockDataset()

        expected = [
            ('A.root', 100), ('B.root', 200), ('C.root', 150), ('D.root', 180), ('E.root', 210)
        ]

        actual = self.obj._file_nevents_list_for(dataset)

        self.assertEqual(expected, actual)

    def test_file_nevents_list_for_maxFiles(self):

        dataset = MockDataset()

        expected = [('A.root', 100)]
        actual = self.obj._file_nevents_list_for(dataset, maxFiles = 1)
        self.assertEqual(expected, actual)

        expected = [ ]
        actual = self.obj._file_nevents_list_for(dataset, maxFiles = 0)
        self.assertEqual(expected, actual)

    def test_create_configs(self):
        dataset = MockDataset()
        file_start_length_list = [('A.root', 0, 40), ('A.root', 40, 40), ('B.root', 0, 10)]
        expected = [
            MockEventBuilderConfig(
                dataset = dataset,
                file_='A.root', start = 0, length = 40
            ),
            MockEventBuilderConfig(
                dataset = dataset,
                file_='A.root', start = 40, length = 40
            ),
            MockEventBuilderConfig(
                dataset = dataset,
                file_='B.root', start=0, length=10
            )
        ]
        actual = self.obj._create_configs(dataset, file_start_length_list)
        self.assertEqual(expected, actual)

    def test_call(self):
        dataset = MockDataset()
        self.obj(dataset)

##__________________________________________________________________||
