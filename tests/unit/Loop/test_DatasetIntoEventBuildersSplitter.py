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
    def file_list_in(self, dataset, maxFiles):
        if maxFiles < 0:
            return dataset.files
        return dataset.files[:min(maxFiles, len(dataset.files))]

    def file_nevents_list_for(self, dataset, maxEvents, maxFiles):
        files = self.file_list_in(dataset, maxFiles = maxFiles)
        totalEvents = 0
        ret = [ ]
        for f, n in zip(files, dataset.nevents):
            if 0 <= maxEvents <= totalEvents:
                return ret
            ret.append((f, n))
            totalEvents += n
        return ret

    def create_config_for(self, dataset, file_, start, length):
        return MockEventBuilderConfig(dataset, file_, start, length)

##__________________________________________________________________||
class TestDatasetIntoEventBuildersSplitter(unittest.TestCase):

    def test_repr(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            )

        repr(obj)

    def test_init_raise(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        self.assertRaises(ValueError,
                          DatasetIntoEventBuildersSplitter,
                          MockEventBuilder,
                          eventBuilderConfigMaker,
                          maxEventsPerRun = 0
        )

    def test_call_default(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            ) # don't give optional arguments

        dataset = MockDataset(
            files = ['A.root', 'B.root'],
            nevents = [100, 200]
        )
        expected = [
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 0,   #
                    length = -1  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 0,   #
                    length = -1  #
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

    def test_call_maxEvents(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            maxEvents = 160,  #
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
                    start = 0,    #
                    length = 100  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 0,    #
                    length = 60   #
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

    def test_call_zero_maxEvents(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            maxEvents = 0, #
            )

        dataset = MockDataset(
            files = ['A.root', 'B.root'],
            nevents = [100, 200]
        )
        expected = [ ] # empty

        actual = obj(dataset)
        self.assertEqual(expected, actual)

    def test_call_maxEventsPerRun(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            maxEventsPerRun = 40, #
            )

        dataset = MockDataset(
            files = ['A.root', 'B.root'],
            nevents = [100, 50]
        )
        expected = [
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 0,   #
                    length = 40  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 40,  #
                    length = 40  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 80,  #
                    length = 20  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 0,   #
                    length = 40  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 40,  #
                    length = 10  #
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

    def test_call_maxEvents_maxEventsPerRun(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            maxEvents = 160,      #
            maxEventsPerRun = 40, #
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
                    start = 0,   #
                    length = 40  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 40,  #
                    length = 40  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 80,  #
                    length = 20  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 0,   #
                    length = 40  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 40,  #
                    length = 20  #
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

    def test_call_maxFiles(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            maxFiles = 1,  #
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
                    start = 0,    #
                    length = -1  #
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

    def test_call_maxEvents_maxEventsPerRun_maxFiles(self):

        eventBuilderConfigMaker = MockEventBuilderConfigMaker()

        obj = DatasetIntoEventBuildersSplitter(
            MockEventBuilder,
            eventBuilderConfigMaker,
            maxEvents = 340,      #
            maxEventsPerRun = 80, #
            maxFiles = 2, #
            )

        dataset = MockDataset(
            files = ['A.root', 'B.root', 'C.root'],
            nevents = [100, 200, 150]
        )
        expected = [
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 0,   #
                    length = 80  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'A.root',
                    start = 80,  #
                    length = 20  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 0,   #
                    length = 80  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 80,  #
                    length = 80  #
                )
            ),
            MockEventBuilder(
                config = MockEventBuilderConfig(
                    dataset = dataset,
                    file_ = 'B.root',
                    start = 160,  #
                    length = 40  #
                )
            ),
        ]
        actual = obj(dataset)
        self.assertEqual(expected, actual)

##__________________________________________________________________||
