# Tai Sakuma <tai.sakuma@cern.ch>

from .functions import *

##__________________________________________________________________||
class Combine(object):
    def combine(self, datasetReaderPairs):
        dataset_summarizer_pairs = [[d, r.results()] for d, r in datasetReaderPairs]
        return add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)

##__________________________________________________________________||
