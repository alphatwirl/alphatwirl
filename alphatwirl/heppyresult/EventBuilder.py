# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.roottree import BEventBuilder
from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='use alphatwirl.roottree.BEventBuilder instead.')
class EventBuilder(object):
    def __init__(self, config):
        self.builder = BEventBuilder(config)
        self.config = config

    def __repr__(self):
        return '{}(config={!r})'.format(
            self.__class__.__name__,
            self.config
        )

    def __call__(self):
        return self.builder()

##__________________________________________________________________||
