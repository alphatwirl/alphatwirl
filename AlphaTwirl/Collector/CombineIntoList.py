# Tai Sakuma <tai.sakuma@cern.ch>

import collections
from functions import *

##__________________________________________________________________||
def summarizer_to_key_vals_dict(summarizer):

    ret = collections.OrderedDict([(k, v.contents) for k, v in summarizer.results().iteritems()])
    # e.g.,
    # OrderedDict([
    #     ((200, 2), [array([120, 240])]),
    #     ((300, 2), [array([490, 980])]),
    #     ((300, 3), [array([210, 420])])
    # ])

    return ret

##__________________________________________________________________||
def summarizer_to_tuple_list(summarizer, sort):

    key_vals_dict = summarizer_to_key_vals_dict(summarizer)
    # e.g.,
    # OrderedDict([
    #     ((200, 2), [array([120, 240])]),
    #     ((300, 2), [array([490, 980])]),
    #     ((300, 3), [array([210, 420])])
    # ])

    tuple_list = convert_key_vals_dict_to_tuple_list(key_vals_dict, fill = 0, sort = sort)
    # e.g.,
    # [
    #     (200, 2, 120, 240),
    #     (300, 2, 490, 980),
    #     (300, 3, 210, 420)
    # ]

    return tuple_list

##__________________________________________________________________||
class CombineIntoList(object):
    def __init__(self, summaryColumnNames,
                 sort = True,
                 datasetColumnName = 'component',
                 summarizer_to_tuple_list = summarizer_to_tuple_list):

        self.summaryColumnNames = summaryColumnNames
        self.sort = sort
        self.datasetColumnName = datasetColumnName
        self.summarizer_to_tuple_list = summarizer_to_tuple_list

    def __repr__(self):
        return '{}(summaryColumnNames = {!r}, sort = {!r}, datasetColumnName = {!r})'.format(
            self.__class__.__name__,
            self.summaryColumnNames,
            self.sort,
            self.datasetColumnName
        )

    def combine(self, datasetReaderPairs):

        if len(datasetReaderPairs) == 0: return None

        # e.g.,
        # datasetReaderPairs = [
        #     ('QCD',    reader1),
        #     ('QCD',    reader2),
        #     ('TTJets', reader3),
        #     ('WJets',  reader4),
        # ]


        dataset_summarizer_pairs = [(d, r.results()) for d, r in datasetReaderPairs]
        # e.g.,
        # dataset_summarizer_pairs = [
        #     ('QCD',    summarizer1),
        #     ('QCD',    summarizer2),
        #     ('TTJets', summarizer3),
        #     ('WJets',  summarizer4),
        # ]

        dataset_summarizer_pairs = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        # e.g.,
        # dataset_summarizer_pairs = [
        #     ('QCD',    summarizer1 + summarizer2),
        #     ('TTJets', summarizer3),
        #     ('WJets',  summarizer4),
        # ]
        # note: summarizers can be added

        dataset_tuple_list_pairs = [ ]
        for dataset, summarizer in dataset_summarizer_pairs:
            tuple_list = self.summarizer_to_tuple_list(summarizer, sort = self.sort)
            dataset_tuple_list_pairs.append((dataset, tuple_list))
        # e.g.,
        # dataset_tuple_list_pairs = [
        #     ('QCD', [
        #         (200, 2, 120, 240),
        #         (300, 2, 490, 980),
        #         (300, 3, 210, 420)
        #     ]),
        #     ('TTJets', [
        #         (300, 2, 20, 40),
        #         (300, 3, 15, 30)
        #     ]),
        #     ('WJets', [])
        # ]

        ret = [ ]
        for dataset, tuple_list in dataset_tuple_list_pairs:
            ret.extend([(dataset, ) + e for e in tuple_list])
        # e.g.,
        # [
        #     ('QCD',    200, 2, 120, 240),
        #     ('QCD',    300, 2, 490, 980),
        #     ('QCD',    300, 3, 210, 420),
        #     ('TTJets', 300, 2,  20,  40),
        #     ('TTJets', 300, 3,  15,  30)
        # ]

        header = (self.datasetColumnName, ) + self.summaryColumnNames

        ret.insert(0, header)
        # e.g.,
        # [
        #     ('dataset', 'htbin', 'njetbin', 'n', 'nvar'),
        #     ('QCD',         200,         2, 120,    240),
        #     ('QCD',         300,         2, 490,    980),
        #     ('QCD',         300,         3, 210,    420),
        #     ('TTJets',      300,         2,  20,     40),
        #     ('TTJets',      300,         3,  15,     30)
        # ]

        return ret

##__________________________________________________________________||
