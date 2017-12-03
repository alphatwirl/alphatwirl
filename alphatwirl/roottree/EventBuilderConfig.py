# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import collections

##__________________________________________________________________||
EventBuilderConfig = collections.namedtuple(
    'EventBuilderConfig',
    'inputPaths treeName maxEvents start name'
)
# 'name' is used by loop.EventLoopProgressReportWriter

##__________________________________________________________________||
