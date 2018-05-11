# Tai Sakuma <tai.sakuma@gmail.com>

try:
    from DataFormats.FWLite import Events as EDMEvents
    # https://github.com/cms-sw/cmssw/blob/CMSSW_9_1_X/DataFormats/FWLite/python/__init__.py
except ImportError:
    pass

from .load_fwlite import load_fwlite

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='alphatwirl.cmsedm has been moved to https://github.com/alphatwirl/atcmsedm.')
class CMSEDMEvents(object):
    def __init__(self, paths, maxEvents = -1, start = 0):
        load_fwlite()

        if start < 0:
            raise ValueError("start must be greater than or equal to zero: {} is given".format(start))

        self.edm_event = EDMEvents(paths)
        # https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/DataFormats/FWLite/python/__init__.py#L457

        nevents_in_dataset = self.edm_event.size()
        start = min(nevents_in_dataset, start)
        if maxEvents > -1:
            self.nEvents = min(nevents_in_dataset - start, maxEvents)
        else:
            self.nEvents = nevents_in_dataset - start
        self.start = start
        self.iEvent = -1

    def __len__(self):
        return self.nEvents

    def __repr__(self):
        return '{}(edm_event = {!r}, maxEvents = {!r}, start = {!r}, nEvents = {!r}, iEvent = {!r})'.format(
            self.__class__.__name__,
            self.edm_event,
            self.maxEvents,
            self.start,
            self.nEvents,
            self.iEvent
        )

    def __iter__(self):
        for self.iEvent in xrange(self.nEvents):
            self.edm_event.to(self.start + self.iEvent)
            yield self
        self.iEvent = -1

##__________________________________________________________________||
