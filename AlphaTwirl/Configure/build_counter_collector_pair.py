# Tai Sakuma <tai.sakuma@cern.ch>
from ..Summary import Reader, Summarizer, NextKeyComposer, KeyValueComposer
from ..CombineIntoList import CombineIntoList
from ..WriteListToFile import WriteListToFile
from ..Loop import Collector

##__________________________________________________________________||
def build_counter_collector_pair(tblcfg):
    keyValComposer = KeyValueComposer(
        keyAttrNames = tblcfg['keyAttrNames'],
        binnings = tblcfg['binnings'],
        keyIndices = tblcfg['keyIndices'],
        valAttrNames = tblcfg['valAttrNames'],
        valIndices = tblcfg['valIndices']
    )
    nextKeyComposer = NextKeyComposer(tblcfg['binnings'])
    summarizer = Summarizer(
        Summary = tblcfg['summaryClass'],
        initial_contents = tblcfg['summaryInitialContents']
    )
    reader = Reader(
        keyValComposer = keyValComposer,
        summarizer = summarizer,
        ## summary = tblcfg['summaryClass'](**tblcfg['summaryClassArgs']),
        nextKeyComposer = nextKeyComposer,
        weightCalculator = tblcfg['weight']
    )
    resultsCombinationMethod = CombineIntoList(
        keyNames = tblcfg['keyOutColumnNames'],
        valNames = tblcfg['valOutColumnNames'],
        sort = tblcfg['sort']
    )
    deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return reader, collector

##__________________________________________________________________||
