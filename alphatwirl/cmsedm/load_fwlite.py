# Tai Sakuma <tai.sakuma@gmail.com>

try:
    import ROOT
except ImportError:
    pass

_loaded = False

##__________________________________________________________________||
def load_fwlite():

    global _loaded
    if _loaded:
        return

    ROOT.gSystem.Load("libFWCoreFWLite")
    ROOT.gSystem.Load("libDataFormatsFWLite")
    ROOT.FWLiteEnabler.enable()

    _loaded = True

##__________________________________________________________________||
