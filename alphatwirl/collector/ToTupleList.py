# Tai Sakuma <tai.sakuma@gmail.com>
import itertools

##__________________________________________________________________||
class ToTupleList(object):
    def __init__(self, summaryColumnNames
                 ):

        self.summaryColumnNames = summaryColumnNames

    def __repr__(self):

        name_value_pairs = (
            ('summaryColumnNames', self.summaryColumnNames),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
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

        readers_list = itertools.chain(*(r for _, r in dataset_readers_list))
        # e.g.,
        # readers_list = (reader1, reader2, reader3, reader4)

        summarizers_list = (r.results() for r in readers_list)
        # e.g.,
        # summarizers_list = (summarizer1, summarizer2, summarizer3, summarizer4)

        summarizer = sum(summarizers_list)

        ret = summarizer.to_tuple_list()
        # e.g.,
        # ret = [
        #         (200, 2, 120, 240),
        #         (300, 2, 490, 980),
        #         (300, 3, 210, 420)
        #         (300, 2, 20, 40),
        #         (300, 3, 15, 30)
        # ]

        ret.insert(0, self.summaryColumnNames)
        # e.g.,
        # [
        #     ('htbin', 'njetbin', 'n', 'nvar'),
        #     (    200,         2, 120,    240),
        #     (    300,         2, 490,    980),
        #     (    300,         3, 210,    420),
        #     (    300,         2,  20,     40),
        #     (    300,         3,  15,     30)
        # ]

        return ret

##__________________________________________________________________||
