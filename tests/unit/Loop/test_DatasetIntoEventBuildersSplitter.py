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

MockDataset = collections.namedtuple('MockDataset', 'files nevents')

##__________________________________________________________________||
class MockEventBuilderConfigMaker(object):
    def file_list_in(self, dataset):
        return dataset.files

    def file_nevents_list_for(self, dataset):
        return zip(dataset.files, dataset.nevents)

    def create_config_for(self, dataset, file_, start, length):
        return MockEventBuilderConfig(dataset, file_, start, length)

##__________________________________________________________________||
class TestDatasetIntoEventBuildersSplitter(unittest.TestCase):

    def test_init_raise(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        self.assertRaises(ValueError,
                          DatasetIntoEventBuildersSplitter,
                          MockEventBuilder,
                          eventBuilderConfigMaker,
                          maxEventsPerRun = 0
        )

    def test_call_nofilesplit(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            )

        dataset = MockDataset(
            files = ['A.root', 'B.root'],
            nevents = [100, 200]
        )
        expected = [
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 0,
                    length = -1
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 0,
                    length = -1
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

    def test_call_filesplit(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            maxEvents = 160,
            maxEventsPerRun = 40,
            )

        dataset = MockDataset(
            files = ['A.root', 'B.root'],
            nevents = [100, 200]
        )
        expected = [
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 0,
                    length = 40
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 40,
                    length = 40
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 80,
                    length = 20
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 0,
                    length = 40
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 40,
                    length = 20
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

##__________________________________________________________________||
