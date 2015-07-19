# Tai Sakuma <tai.sakuma@cern.ch>
from ..Counter import GenericKeyComposerBFactory
from ..Counter import CounterFactory
from ..CombineIntoList import CombineIntoList
from ..WriteListToFile import WriteListToFile
from ..EventReader import Collector
from ..EventReader import EventReaderCollectorAssociator

##__________________________________________________________________||
class EventReaderCollectorAssociatorBuilder(object):
    def build(self, tblcfg):
        keyComposerFactory = GenericKeyComposerBFactory(tblcfg['branchNames'], tblcfg['binnings'], tblcfg['indices'])
        counterFactory = CounterFactory(
            countMethodClass = tblcfg['countsClass'],
            keyComposerFactory = keyComposerFactory,
            binnings = tblcfg['binnings'],
            weightCalculator = tblcfg['weight']
        )
        resultsCombinationMethod = CombineIntoList(keyNames = tblcfg['outColumnNames'])
        deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
        collector = Collector(resultsCombinationMethod, deliveryMethod)
        return EventReaderCollectorAssociator(counterFactory, collector)

##__________________________________________________________________||
