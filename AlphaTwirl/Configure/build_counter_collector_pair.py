# Tai Sakuma <tai.sakuma@cern.ch>
from ..Counter import Summarizer, NextKeyComposer, KeyValueComposer
from ..CombineIntoList import CombineIntoList
from ..WriteListToFile import WriteListToFile
from ..EventReader import Collector

##__________________________________________________________________||
def build_counter_collector_pair(tblcfg):
    keyValComposer = KeyValueComposer(
        keyAttrNames = tblcfg['branchNames'],
        binnings = tblcfg['binnings'],
        keyIndices = tblcfg['indices']
    )
    nextKeyComposer = NextKeyComposer(tblcfg['binnings'])
    summarizer = Summarizer(
        keyValComposer = keyValComposer,
        summary = tblcfg['countsClass'](),
        nextKeyComposer = nextKeyComposer,
        weightCalculator = tblcfg['weight']
    )
    resultsCombinationMethod = CombineIntoList(keyNames = tblcfg['outColumnNames'], valNames = ('n', 'nvar'))
    deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return summarizer, collector

##__________________________________________________________________||
