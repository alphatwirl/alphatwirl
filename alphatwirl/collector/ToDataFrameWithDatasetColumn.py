# Tai Sakuma <tai.sakuma@gmail.com>

import pandas as pd

from .ToTupleListWithDatasetColumn import ToTupleListWithDatasetColumn

##__________________________________________________________________||
class ToDataFrameWithDatasetColumn(object):
    def __init__(self, summaryColumnNames,
                 datasetColumnName = 'component'
                 ):

        self.summaryColumnNames = summaryColumnNames
        self.datasetColumnName = datasetColumnName
        self.to_tuple_list = ToTupleListWithDatasetColumn(
            summaryColumnNames = summaryColumnNames,
            datasetColumnName = datasetColumnName)

    def __repr__(self):

        name_value_pairs = (
            ('summaryColumnNames', self.summaryColumnNames),
            ('datasetColumnName',  self.datasetColumnName),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def combine(self, dataset_readers_list):
        tuple_list = self.to_tuple_list.combine(dataset_readers_list)
        if tuple_list is None:
            return None
        header = tuple_list[0]
        contents = tuple_list[1:]
        return pd.DataFrame(contents, columns = header)

##__________________________________________________________________||
