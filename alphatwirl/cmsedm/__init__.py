inCMSENV = False
try:
    import ROOT
    from DataFormats.FWLite import Handle
    from DataFormats.FWLite import Events as EDMEvents
    # https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/DataFormats/FWLite/python/__init__.py
    inCMSENV = True
except ImportError:
    pass

if inCMSENV:
    from CMSEDMEvents import CMSEDMEvents
    from CMSEDMEventBuilder import CMSEDMEventBuilder
    from EventBuilderConfigMaker import EventBuilderConfigMaker
