import unittest

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.delphes import DelphesEvents

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestDelphesEvents(unittest.TestCase):
    pass

##__________________________________________________________________||
