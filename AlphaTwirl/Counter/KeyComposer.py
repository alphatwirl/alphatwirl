# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class KeyComposer_SingleVariable(object):
    def __init__(self, varName, binning):
        self._varName = varName
        self._binning = binning

    def __call__(self, event):
        var = getattr(event, self._varName)
        var_bin = self._binning(var)
        return (var_bin, )

    def binnings(self):
        return (self._binning, )

##____________________________________________________________________________||
class KeyComposer_TwoVariables(object):
    def __init__(self, varName1, binning1, varName2, binning2):
        self._varName1 = varName1
        self._binning1 = binning1
        self._varName2 = varName2
        self._binning2 = binning2

    def __call__(self, event):
        var1 = getattr(event, self._varName1)
        var1_bin = self._binning1(var1)
        var2 = getattr(event, self._varName2)
        var2_bin = self._binning2(var2)
        return (var1_bin, var2_bin)

    def binnings(self):
        return (self._binning1, self._binning2)

##____________________________________________________________________________||
