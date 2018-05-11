# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import os.path

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class ReadVersionInfo(object):
    def __call__(self, path):
        if not os.path.isfile(path): return None
        file = open(path)
        return self._readImp(file)

    def _readImp(self, file):
        full = file.read()
        # versionInfo.txt is written as
        # https://github.com/CMSRA1/cmg-cmssw-private/blob/RA1cmg_v2.4_patch1/CMGTools/Production/scripts/heppyBatchAlphaT.py#L91
        # the second line will be the tag
        tag = full.split(b'\n')[1]
        print(tag)
        return dict(full = full, tag = tag)

##__________________________________________________________________||
