# Tai Sakuma <tai.sakuma@gmail.com>

import collections

##__________________________________________________________________||
class TClonesArrayWrap(collections.Sequence):
    """wrap TClonesArray for fast access"

       (under development. not used)

    """
    def __init__(self, tclonesarray):
        self.tclonesarray = tclonesarray
        self.name = self.tclonesarray.GetName()
        self.max_length = tclonesarray.GetSize()
        self.extracted_length = 0
        self.list = [ ]

    def _GetEntries(self):
        ## return self.tclonesarray.GetEntries() # very slow
        return self.tclonesarray.GetEntriesFast() # faster but still very slow

    def __getitem__(self, i):
        nentries = self._GetEntries()
        if i >= nentries:
            raise IndexError('the index is out of range: {}[{}]'.format(self.name, i))
        if self.extracted_length < nentries:
            ## print self.extracted_length, nentries
            self.list[self.extracted_length:] = [self.tclonesarray.At(i) for i in range(self.extracted_length, nentries)]
            self.extracted_length = nentries
        return self.list[i]

    def __len__(self):
        return self.tclonesarray.GetEntriesFast()

##__________________________________________________________________||
