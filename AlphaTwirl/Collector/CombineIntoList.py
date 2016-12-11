# Tai Sakuma <tai.sakuma@cern.ch>

import collections
from functions import *

##__________________________________________________________________||
def combinedToList(dataset_summarizer_pairs, columns, sort = True):

    dataset_key_vals_dict_pairs = [ ]
    for datasetName, summarizer in dataset_summarizer_pairs:
        key_vals_dict = collections.OrderedDict([(k, v.contents) for k, v in summarizer.results().iteritems()])
        dataset_key_vals_dict_pairs.append((datasetName, key_vals_dict))

    d = [ ]
    for datasetName, key_vals_dict in dataset_key_vals_dict_pairs:
        l = convert_key_vals_dict_to_tuple_list(key_vals_dict, fill = 0, sort = sort)
        d.extend([(datasetName, ) + e for e in l])

    if sort: d.sort()

    d.insert(0, columns)

    return d

##__________________________________________________________________||
class CombineIntoList(object):
    def __init__(self, keyNames, valNames, sort = True):
        self.datasetColumnName = 'component'
        self.keyNames = keyNames
        self.valNames = valNames
        self.sort = sort

    def combine(self, datasetReaderPairs):
        if len(datasetReaderPairs) == 0: return None
        dataset_summarizer_pairs = [(d, r.results()) for d, r in datasetReaderPairs]
        dataset_summarizer_pairs = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        return combinedToList(
            dataset_summarizer_pairs,
            (self.datasetColumnName, ) + self.keyNames + self.valNames,
            self.sort
        )

##__________________________________________________________________||
