# Tai Sakuma <tai.sakuma@gmail.com>
from atpbar import atpbar

##__________________________________________________________________||
class CollectorComposite(object):
    """A composite of collectors

    To be paired with `alphatwirl.loop.ReaderComposite`

    """

    def __init__(self):
        self.components = [ ]

    def add(self, collector):
        self.components.append(collector)

    def __call__(self, dataset_result_list):
        dataset_result_list = self._rearrange(dataset_result_list)
        ret = [
            collector(r) for collector, r
            in zip(atpbar(self.components, name='collecting results'), dataset_result_list)
        ]
        return ret

    def _rearrange(self, dataset_result_list):

        # e.g., dataset_result_list = [
        #     ['QCD',    [result11, result21, result31]],
        #     ['TTJets', [result12, result22, result32]],
        #     ['WJets',  [result13, result23, result33]],
        # ]

        ret = [
            [(d, r) for r in readers]
            for d, readers in dataset_result_list]
        # e.g., [
        #     [('QCD',    result11), ('QCD',    result21), ('QCD',    result31)],
        #     [('TTJets', result12), ('TTJets', result22), ('TTJets', result32)],
        #     [('WJets',  result13), ('WJets',  result23), ('WJets',  result33)]
        # ]

        ret = list(map(tuple, zip(*ret)))
        # [
        #     [('QCD', result11), ('TTJets', result12), ('WJets', result13)],
        #     [('QCD', result21), ('TTJets', result22), ('WJets', result23)],
        #     [('QCD', result31), ('TTJets', result32), ('WJets', result33)],
        # ]

        return ret

##__________________________________________________________________||
