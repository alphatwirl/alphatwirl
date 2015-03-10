# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class GenericKeyComposer(object):
    def __init__(self, varNames, binnings):
        self._varNames = varNames
        self._binnings = binnings

    def __call__(self, event):
        ret = [ ]
        for varName, binning in zip(self._varNames, self._binnings):
            var = getattr(event, varName)
            var_bin = binning(var)
            if var_bin is None: return None
            ret.append(var_bin)
        return tuple(ret)

    def binnings(self):
        return self._binnings

##____________________________________________________________________________||
class KeyComposer_SingleVariable(object):
    def __init__(self, varName, binning):
        self._composer = GenericKeyComposer((varName, ), (binning, ))

    def __call__(self, event):
        return self._composer(event)

    def binnings(self):
        return self._composer.binnings()

##____________________________________________________________________________||
class KeyComposer_TwoVariables(object):
    def __init__(self, varName1, binning1, varName2, binning2):
        self._composer = GenericKeyComposer((varName1, varName2), (binning1, binning2))

    def __call__(self, event):
        return self._composer(event)

    def binnings(self):
        return self._composer.binnings()

##____________________________________________________________________________||
