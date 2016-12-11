# Tai Sakuma <tai.sakuma@cern.ch>

import collections
from functions import *

##__________________________________________________________________||
class CombineIntoList(object):
    def __init__(self, keyNames, valNames, sort = True, datasetColumnName = 'component'):
        self.keyNames = keyNames
        self.valNames = valNames
        self.sort = sort
        self.datasetColumnName = datasetColumnName

    def __repr__(self):
        return '{}(keyNames = {!r}, valNames = {!r}, sort = {!r}, datasetColumnName = {!r})'.format(
            self.__class__.__name__,
            self.keyNames,
            self.valNames,
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

        dataset_key_vals_dict_pairs = [ ]
        for dataset, summarizer in dataset_summarizer_pairs:
            key_vals_dict = collections.OrderedDict([(k, v.contents) for k, v in summarizer.results().iteritems()])
            dataset_key_vals_dict_pairs.append((dataset, key_vals_dict))
        # e.g.,
        # dataset_key_vals_dict_pairs = [
        #     ('QCD', OrderedDict([
        #         ((200, 2), [array([120, 240])]),
        #         ((300, 2), [array([490, 980])]),
        #         ((300, 3), [array([210, 420])])
        #     ])),
        #     ('TTJets', OrderedDict([
        #         ((300, 2), [array([20, 40])]),
        #         ((300, 3), [array([15, 30])])
        #     ])),
        #     ('WJets', OrderedDict())
        # ]

        dataset_tuple_list_pairs = [ ]
        for dataset, key_vals_dict in dataset_key_vals_dict_pairs:
            tuple_list = convert_key_vals_dict_to_tuple_list(key_vals_dict, fill = 0, sort = self.sort)
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

        if self.sort: ret.sort()

        header = (self.datasetColumnName, ) + self.keyNames + self.valNames

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
