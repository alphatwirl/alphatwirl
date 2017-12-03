# Tai Sakuma <tai.sakuma@gmail.com>

import pandas as pd

from .ToTupleList import ToTupleList

##__________________________________________________________________||
class ToDataFrame(object):
    def __init__(self, summaryColumnNames):

        self.summaryColumnNames = summaryColumnNames
        self.to_tuple_list = ToTupleList(summaryColumnNames = summaryColumnNames)

    def __repr__(self):

        name_value_pairs = (
            ('summaryColumnNames', self.summaryColumnNames),
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
