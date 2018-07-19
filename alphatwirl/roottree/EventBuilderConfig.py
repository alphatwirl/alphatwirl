# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import collections

##__________________________________________________________________||
# EventBuilderConfig is deprecated as EventBuilder is being replaced
# with BuildEvents, which uses dict instead of EventBuilderConfig

EventBuilderConfig = collections.namedtuple(
    'EventBuilderConfig',
    'inputPaths treeName maxEvents start name'
)
# 'name' is used by loop.EventLoopProgressReportWriter

##__________________________________________________________________||
