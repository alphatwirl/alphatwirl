# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import os
import ast
import logging

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class ReadComponentConfig(object):
    def __call__(self, path):
        if not os.path.isfile(path):
            logging.warning('cannot open {}'.format(path))
            return None
        file = open(path)
        return self._readImp(file)

    def _readImp(self, file):
        file.readline() # skip the 1st line
        l = [[e.strip() for e in l.split(b":", 1)] for l in file]
        return dict([(e[0], self._literal_eval_or_string(e[1])) for e in l])

    def _literal_eval_or_string(self, val):
        try:
            return ast.literal_eval(val.decode())
        except:
            return val

##__________________________________________________________________||
