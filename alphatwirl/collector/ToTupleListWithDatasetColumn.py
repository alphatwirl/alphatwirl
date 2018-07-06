# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ToTupleListWithDatasetColumn(object):
    def __init__(self, summaryColumnNames,
                 datasetColumnName='component'
                 ):

        self.summaryColumnNames = summaryColumnNames
        self.datasetColumnName = datasetColumnName

        self._repr_pairs = [
            ('summaryColumnNames', self.summaryColumnNames),
            ('datasetColumnName',  self.datasetColumnName),
        ]

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self._repr_pairs]),
        )

    def combine(self, dataset_readers_list):


        if len(dataset_readers_list) == 0: return None

        # e.g.,
        # dataset_readers_list = [
        #     ('QCD',    (reader1, reader2)),
        #     ('TTJets', (reader3, )),
        #     ('WJets',  (reader4, )),
        #     ('ZJets',  ( )),
        # ]

        # remove entries with no readers
        dataset_readers_list = [l for l in dataset_readers_list if l[1]]
        if len(dataset_readers_list) == 0: return None

        dataset_summarizers_list = [(d, tuple(r.results() for r in rs)) for d, rs in dataset_readers_list]
        # e.g.,
        # dataset_summarizers_list = [
        #     ('QCD',    (summarizer1, summarizer2)),
        #     ('TTJets', (summarizer3, ),
        #     ('WJets',  (summarizer4, ),
        # ]

        dataset_summarizer_pairs = [(d, sum(s)) for d, s in  dataset_summarizers_list]
        # e.g.,
        # dataset_summarizer_pairs = [
        #     ('QCD',    summarizer1 + summarizer2),
        #     ('TTJets', summarizer3),
        #     ('WJets',  summarizer4),
        # ]
        # note: summarizers can be added

        dataset_tuple_list_pairs = [(d, s.to_tuple_list()) for d, s in dataset_summarizer_pairs]
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
