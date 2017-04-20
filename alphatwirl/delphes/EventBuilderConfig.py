# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import collections

##__________________________________________________________________||
EventBuilderConfig = collections.namedtuple(
    'EventBuilderConfig',
    'inputPath treeName maxEvents start dataset name'
)

##__________________________________________________________________||
