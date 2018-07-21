# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.roottree import Events

##__________________________________________________________________||
class MockFile(object):
    pass

class MockTree(object):
    def __init__(self, entries=100):
        self.entries = entries
        self.ievent = -1
        self.branchstatus = [ ]
        self.branch1 = 1111
        self.directory = MockFile()
    def GetDirectory(self):
        return self.directory
    def GetEntries(self):
        return self.entries
    def GetEntry(self, ientry):
        if ientry < self.entries:
            nbytes = 10
            self.ievent = ientry
        else:
            nbytes = 0
            self.ievent = -1
        return nbytes

    def SetBranchStatus(self, bname, status):
        self.branchstatus.append((bname, status))

def test_mocktree():

    tree = MockTree(entries=3)
    assert isinstance(tree.GetDirectory(), MockFile)
    assert 3 == tree.GetEntries()

    assert -1 == tree.ievent

    nbytes = 10
    assert nbytes == tree.GetEntry(0)
    assert 0 == tree.ievent
    assert nbytes == tree.GetEntry(1)
    assert 1 == tree.ievent
    assert nbytes == tree.GetEntry(2)
    assert 2 == tree.ievent
    assert 0 == tree.GetEntry(3)
    assert -1 == tree.ievent

##__________________________________________________________________||
def test_iter_getattr():
    tree = MockTree(entries=5)
    events = Events(tree)
    it = iter(events)
    event = next(it)
    assert 1111 == event.branch1
    tree.branch1 = 2222
    assert 2222 == event.branch1

##__________________________________________________________________||
