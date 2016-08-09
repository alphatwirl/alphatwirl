# Tai Sakuma <tai.sakuma@cern.ch>
from ..Summary import Summarizer, NextKeyComposer, KeyValueComposer
from ..CombineIntoList import CombineIntoList
from ..WriteListToFile import WriteListToFile
from ..Loop import Collector

##__________________________________________________________________||
def build_counter_collector_pair(tblcfg):
    keyValComposer = KeyValueComposer(
        keyAttrNames = tblcfg['keyAttrNames'],
        binnings = tblcfg['binnings'],
        keyIndices = tblcfg['keyIndices']
    )
    nextKeyComposer = NextKeyComposer(tblcfg['binnings'])
    summarizer = Summarizer(
        keyValComposer = keyValComposer,
        summary = tblcfg['summaryClass'](),
        nextKeyComposer = nextKeyComposer,
        weightCalculator = tblcfg['weight']
    )
    resultsCombinationMethod = CombineIntoList(keyNames = tblcfg['outColumnNames'], valNames = ('n', 'nvar'))
    deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return summarizer, collector

##__________________________________________________________________||
