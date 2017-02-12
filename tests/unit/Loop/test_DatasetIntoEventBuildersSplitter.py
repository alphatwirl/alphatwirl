import sys
import collections
import unittest

from AlphaTwirl.Loop import DatasetIntoEventBuildersSplitter

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

    def __call__(self, file_nevents_list, max_per_run = -1, max_total = -1):
        self.args_call.append((file_nevents_list, max_per_run, max_total))
        return self.ret

##__________________________________________________________________||
class MockEventBuilderConfigMaker(object):
    def __init__(self):
        self.args_file_list_in = [ ]
        self.args_file_nevents_list_for = [ ]
        self.args_create_config_for = [ ]
        self.ret_file_list_in = None
        self.ret_file_nevents_list_for = None
        self.ret_create_config_for = None

    def file_list_in(self, dataset, maxFiles):
        self.args_file_list_in.append((dataset, maxFiles))
        return self.ret_file_list_in

    def file_nevents_list_for(self, dataset, maxEvents, maxFiles):
        self.args_file_nevents_list_for.append((dataset, maxEvents, maxFiles))
        return  self.ret_file_nevents_list_for

    def create_config_for(self, dataset, file_, start, length):
        self.args_create_config_for.append((dataset, file_, start, length))
        return MockEventBuilderConfig(dataset, file_, start, length)

##__________________________________________________________________||
class TestDatasetIntoEventBuildersSplitter(unittest.TestCase):

    def setUp(self):
        self.configMaker = MockEventBuilderConfigMaker()
        self.configMaker.ret_file_list_in = ['A.root', 'B.root']
        self.configMaker.ret_file_nevents_list_for = [('A.root', 100), ('B.root', 200)]

        self.obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            self.configMaker,
            )

        self.split_func = MockSplitFunc()
        self.split_func.ret = [('A.root', 0, 40), ('A.root', 40, 40), ('A.root', 80, 20), ('B.root', 0, 10)]
        self.obj.create_file_start_length_list = self.split_func

    def test_repr(self):
        repr(self.obj)

    def test_init_raise(self):
        configMaker = MockEventBuilderConfigMaker()
        self.assertRaises(ValueError,
                          DatasetIntoEventBuildersSplitter,
                          MockEventBuilder,
                          configMaker,
                          maxEventsPerRun = 0
        )

    def test_file_start_length_list_fast_path(self):
        dataset = MockDataset()
        maxEvents = -1        # < 0
        maxEventsPerRun = -1  # < 0
        maxFiles = 5
        expected = [('A.root', 0, -1), ('B.root', 0, -1)]
        actual = self.obj._file_start_length_list(dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun, maxFiles = maxFiles)
        self.assertEqual([(dataset, 5)], self.configMaker.args_file_list_in)
        self.assertEqual([ ], self.configMaker.args_file_nevents_list_for)
        self.assertEqual([ ], self.configMaker.args_create_config_for)
        self.assertEqual([ ], self.split_func.args_call)
        self.assertEqual(expected, actual)

    def test_file_start_length_list_long_path(self):
        dataset = MockDataset()
        maxEvents = 110        # >= 0
        maxEventsPerRun = 40   # >= 0
        maxFiles = 5
        expected = [('A.root', 0, 40), ('A.root', 40, 40), ('A.root', 80, 20), ('B.root', 0, 10)]
        actual = self.obj._file_start_length_list(dataset, maxEvents = maxEvents, maxEventsPerRun = maxEventsPerRun, maxFiles = maxFiles)
        self.assertEqual([ ], self.configMaker.args_file_list_in)
        self.assertEqual([(dataset, 110, 5)], self.configMaker.args_file_nevents_list_for)
        self.assertEqual([ ], self.configMaker.args_create_config_for)
        self.assertEqual([([('A.root', 100), ('B.root', 200)], 40, 110)], self.split_func.args_call)

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
