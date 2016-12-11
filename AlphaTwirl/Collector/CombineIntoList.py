# Tai Sakuma <tai.sakuma@cern.ch>

import collections
from functions import *

##__________________________________________________________________||
class CombineIntoList(object):
    def __init__(self, keyNames, valNames, sort = True):
        self.datasetColumnName = 'component'
        self.keyNames = keyNames
        self.valNames = valNames
        self.sort = sort

    def combine(self, datasetReaderPairs):

        if len(datasetReaderPairs) == 0: return None

        # e.g.,
        # datasetReaderPairs = [
        #     ('dataset1', reader),
        #     ('dataset1', reader),
        #     ('dataset2', reader),
        #     ('dataset2', reader),
        #     ('dataset3', reader),
        #     ('dataset3', reader)
        # ]

        dataset_summarizer_pairs = [(d, r.results()) for d, r in datasetReaderPairs]
        # e.g.,
        # dataset_summarizer_pairs = [
        #     ('dataset1', summarizer),
        #     ('dataset1', summarizer),
        #     ('dataset2', summarizer),
        #     ('dataset2', summarizer),
        #     ('dataset3', summarizer),
        #     ('dataset3', summarizer)
        # ]

        dataset_summarizer_pairs = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        # e.g.,
        # dataset_summarizer_pairs = [
        #     ('dataset1', summarizer),
        #     ('dataset2', summarizer),
        #     ('dataset3', summarizer)
        # ]

        dataset_key_vals_dict_pairs = [ ]
        for dataset, summarizer in dataset_summarizer_pairs:
            key_vals_dict = collections.OrderedDict([(k, v.contents) for k, v in summarizer.results().iteritems()])
            dataset_key_vals_dict_pairs.append((dataset, key_vals_dict))
        # e.g.,
        # dataset_key_vals_dict_pairs = [
        #     ('dataset1', {key1: [val11, val12], key2: [ ], key3: [val31]}),
        #     ('dataset2', {key1: [val11], key2: [val21, val22], key3: [val31]}),
        #     ('dataset3', {key1: [val11, val12, val123], key2: [val2]}),
        # ]
        # key and val are general tuples

        dataset_tuple_list_pairs = [ ]
        for dataset, key_vals_dict in dataset_key_vals_dict_pairs:
            tuple_list = convert_key_vals_dict_to_tuple_list(key_vals_dict, fill = 0, sort = self.sort)
            dataset_tuple_list_pairs.append((dataset, tuple_list))
        # e.g.,
        # dataset_tuple_list_pairs = [
        #     ('dataset1', [ ]),
        #     ('dataset2', [ ]),
        #     ('dataset3', [ ]),
        # ]

        ret = [ ]
        for dataset, tuple_list in dataset_tuple_list_pairs:
            ret.extend([(dataset, ) + e for e in tuple_list])

        if self.sort: ret.sort()

        ## import pprint
        ## pprint.pprint(ret)

        header = (self.datasetColumnName, ) + self.keyNames + self.valNames

        ret.insert(0, header)

        return ret

##__________________________________________________________________||
