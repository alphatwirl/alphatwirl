import unittest
import sys

from alphatwirl.heppyresult import EventBuilderConfig

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.heppyresult.EventBuilder import EventBuilder
    # depends on ROOT through roottree.BEventBuilder

##__________________________________________________________________||
class MockEvents(object):
    def __init__(self, config):
        self.config = config

##__________________________________________________________________||
class MockComponent(object):
    pass

##__________________________________________________________________||
class MockBaseEventBuilder(object):

    def __init__(self, config):
        self.config = config

    def __call__(self):
        return MockEvents(self.config)

##__________________________________________________________________||
class MockBaseConfig(object):
    pass

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestEventBuilder(unittest.TestCase):

    def setUp(self):
        self.module = sys.modules['alphatwirl.heppyresult.EventBuilder']
        self.org_BaseEventBuilder = self.module.BaseEventBuilder
        self.module.BaseEventBuilder = MockBaseEventBuilder

    def tearDown(self):
        self.module.BaseEventBuilder = self.org_BaseEventBuilder

    def test_build(self):

        base_config = MockBaseConfig
        component = MockComponent()

        config = EventBuilderConfig(
            base = base_config,
            component = component,
        )

        obj = EventBuilder(config)

        events = obj()

        self.assertIs(base_config, events.config)
        self.assertIs(component, events.component)

##__________________________________________________________________||
