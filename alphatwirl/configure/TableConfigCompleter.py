# Tai Sakuma <tai.sakuma@gmail.com>
import os
from .TableFileNameComposer import TableFileNameComposer
from ..summary import Count, WeightCalculatorOne

##__________________________________________________________________||
class TableConfigCompleter(object):
    """
    an example complete config::

        tblcfg = {
            'keyAttrNames': ('met_pt',),
            'binnings': (MockBinning(),),
            'keyIndices': None
            'valAttrNames' : None,
            'valIndices' : None,
            'keyOutColumnNames': ('met_pt',),
            'valOutColumnNames': ('n', 'nvar'),
            'weight': MockWeight(),
            'summaryClass': Count,
            'sort': True,
            'outFile': True,
            'outFileName': 'tbl_n_component_met_pt.txt',
            'outFilePath': '/tmp/tbl_n_component_met_pt.txt',
        }

    """
    def __init__(self,
                 defaultSummaryClass=Count,
                 defaultWeight=WeightCalculatorOne(),
                 defaultOutDir='.',
                 createOutFileName=TableFileNameComposer()):

        self.defaultSummaryClass = defaultSummaryClass
        self.defaultWeight = defaultWeight
        self.defaultOutDir = defaultOutDir
        self.createOutFileName = createOutFileName

        self.default_cfg = dict(
            keyAttrNames=( ),
            binnings=None,
            keyIndices=None,
            valAttrNames=None,
            valIndices=None,
            summaryClass=defaultSummaryClass,
            weight=defaultWeight,
            outFile=True,
            sort=True,
            nevents=None,
        )

    def __repr__(self):
        name_value_pairs = (
            ('defaultSummaryClass', self.defaultSummaryClass),
            ('defaultWeight', self.defaultWeight),
            ('defaultOutDir', self.defaultOutDir),
            ('createOutFileName', self.createOutFileName),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def complete(self, tblcfg):
        ret = self.default_cfg.copy()
        ret.update(tblcfg)

        use_defaultSummaryClass = 'summaryClass' not in tblcfg

        ret['keyOutColumnNames'] = ret.get('keyOutColumnNames', ret['keyAttrNames'])
        # TODO: this line is not tested well. The following code also passes the tests
        # ret['keyOutColumnNames'] = ret.get('keyAttrNames', ret['keyAttrNames'])

        if 'valOutColumnNames' not in ret:
            if use_defaultSummaryClass:
                ret['valOutColumnNames'] = ('n', 'nvar')
            else:
                ret['valOutColumnNames'] = ret['valAttrNames'] if ret['valAttrNames'] is not None else ()

        if ret['outFile']:
            if 'outFileName' not in ret:
                if use_defaultSummaryClass:
                    ret['outFileName'] = self.createOutFileName(
                        ret['keyOutColumnNames'], ret['keyIndices']
                    )
                else:
                    keyOutColumnNames  = ret['keyOutColumnNames'] if ret['keyOutColumnNames'] is not None else ()
                    keyIndices = ret['keyIndices'] if ret['keyIndices'] is not None else (None, )*len(keyOutColumnNames)
                    valOutColumnNames  = ret['valOutColumnNames'] if ret['valOutColumnNames'] is not None else ()
                    valIndices = ret['valIndices'] if ret['valIndices'] is not None else (None, )*len(valOutColumnNames)
                    ret['outFileName'] = self.createOutFileName(
                        keyOutColumnNames + valOutColumnNames,
                        keyIndices + valIndices,
                        prefix='tbl_{}'.format(ret['summaryClass'].__name__)
                    )
            if 'outFilePath' not in ret:
                ret['outFilePath'] = os.path.join(self.defaultOutDir, ret['outFileName'])
        return ret

##__________________________________________________________________||
