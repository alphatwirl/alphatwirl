# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import re
import collections
import ast
import os

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class ReadCounter(object):
    def __call__(self, path):
        if not os.path.isfile(path): return None
        file = open(path)
        return self._readImp(file)

    def _readImp(self, file):
        counter = collections.OrderedDict()

        file.readline() # skip the 1st line
        for line in file:
            level, content = self._readLine(line)
            if level is None: continue
            counter[level] = content
        return counter

    def _readLine(self, line):
        # a line is written in the format '\t {level:<40} {count:>9} \t {eff1:4.2f} \t {eff2:6.4f}\n'
        # https://github.com/cms-sw/cmssw/blob/CMSSW_7_4_0/PhysicsTools/HeppyCore/python/statistics/counter.py
        exp = r'^\t (.*?) *([0-9e+-.]*) \t ([0-9e+-.]*) \t ([0-9e+-.]*)$'
        exp = exp.encode()
        match = re.search(exp, line)

        if not match: return None, None
        level = match.group(1)
        count = match.group(2)
        eff1 =  match.group(3)
        eff2 = match.group(4)
        count = count.decode()
        return level, dict(count = ast.literal_eval(count), eff1 = float(eff1), eff2 = float(eff2))

##__________________________________________________________________||
