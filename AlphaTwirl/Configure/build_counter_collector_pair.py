# Tai Sakuma <tai.sakuma@cern.ch>
from ..Counter import Counter, GenericKeyComposerB, NextKeyComposer
from ..CombineIntoList import CombineIntoList
from ..WriteListToFile import WriteListToFile
from ..EventReader import Collector

##__________________________________________________________________||
def build_counter_collector_pair(tblcfg):
    keyComposer = GenericKeyComposerB(tblcfg['branchNames'], tblcfg['binnings'], tblcfg['indices'])
    nextKeyComposer = NextKeyComposer(tblcfg['binnings'])
    counter = Counter(
        keyComposer = keyComposer,
        countMethod = tblcfg['countsClass'](),
        nextKeyComposer = nextKeyComposer,
        weightCalculator = tblcfg['weight']
    )
    resultsCombinationMethod = CombineIntoList(keyNames = tblcfg['outColumnNames'])
    deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return counter, collector

##__________________________________________________________________||
