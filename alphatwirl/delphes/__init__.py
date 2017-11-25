hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from .DelphesEvents import DelphesEvents
    from .DelphesEventBuilder import DelphesEventBuilder
    from .EventBuilderConfigMaker import EventBuilderConfigMaker
