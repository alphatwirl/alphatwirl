# Tai Sakuma <tai.sakuma@gmail.com>
import os
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from alphatwirl.roottree import BEvents as Events

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
class MockFile(object):
    pass

##__________________________________________________________________||
class MockTree(object):
    def __init__(self, entries=100):
        self.entries = entries
        self.ievent = -1
        self.branchstatus = [ ]
        self.getEntry_called = False
        self.directory = MockFile()
    def GetDirectory(self):
        return self.directory
    def GetEntries(self):
        return self.entries
    def GetEntry(self, ientry):
        self.getEntry_called = True
        if ientry < self.entries:
            nbytes = 10
            self.ievent = ientry
        else:
            nbytes = 0
            self.ievent = -1
        return nbytes

    def SetBranchStatus(self, bname, status):
        self.branchstatus.append((bname, status))

##__________________________________________________________________||
class MockBranch(object):
    pass

##__________________________________________________________________||
class MockBranchBuilder(object):
    def __init__(self):
        self.next = None
    def __call__(self, tree, name):
        return self.next

##__________________________________________________________________||
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
def test_repr():
    tree = MockTree()
    events = Events(tree)
    repr(events)

def test_init_branch_status():
    tree = MockTree()
    assert [ ] == tree.branchstatus
    events = Events(tree)
    events.buildBranch = MockBranchBuilder()
    assert [('*', 0)] == tree.branchstatus

def test_getattr():
    tree = MockTree()
    events = Events(tree)
    branchBuilder = MockBranchBuilder()
    events.buildBranch = branchBuilder

    branchBuilder.next = MockBranch()
    jet_pt = events.jet_pt
    assert isinstance(jet_pt, MockBranch)

def test_getattr_same_objects():
    tree = MockTree()
    events = Events(tree)
    branchBuilder = MockBranchBuilder()
    events.buildBranch = branchBuilder

    branch1 = MockBranch()
    branchBuilder.next = branch1
    jet_pt1 = events.jet_pt
    assert branch1 is jet_pt1

    branch2 = MockBranch()
    branchBuilder.next = branch2
    jet_pt2 = events.jet_pt

    assert branch1 is jet_pt2
    assert branch2 is not jet_pt2

    it = iter(events)
    event = next(it)

    branch3 = MockBranch()
    branchBuilder.next = branch3
    jet_pt3 = event.jet_pt

    assert branch1 is jet_pt3
    assert branch3 is not jet_pt3

def test_getattr_exception():
    tree = MockTree()
    events = Events(tree)
    events.buildBranch = MockBranchBuilder()

    with pytest.raises(AttributeError):
        events.no_such_branch

def test_getattr_getentry():
    tree = MockTree()
    events = Events(tree, start=10)
    branchBuilder = MockBranchBuilder()
    events.buildBranch = branchBuilder

    assert -1 == events.iEvent
    assert -1 == tree.ievent
    assert not tree.getEntry_called
    branchBuilder.next = MockBranch()
    jet_pt = events.jet_pt
    assert not tree.getEntry_called

    it = iter(events)
    event = next(it)
    tree.getEntry_called = False
    assert 0 == events.iEvent
    assert 10 == tree.ievent
    assert not tree.getEntry_called
    jet_pt = event.jet_pt
    assert not tree.getEntry_called

    tree.getEntry_called = False
    met_pt = event.met_pt
    assert tree.getEntry_called
    assert 0 == events.iEvent
    assert 10 == tree.ievent

    event = next(it)
    tree.getEntry_called = False
    assert 1 == events.iEvent
    assert 11 == tree.ievent
    assert not tree.getEntry_called
    jet_pt = event.jet_pt
    assert not tree.getEntry_called

    tree.getEntry_called = False
    met_pt = event.met_pt
    assert not tree.getEntry_called
    assert 1 == events.iEvent
    assert 11 == tree.ievent

    tree.getEntry_called = False
    njets = event.njets
    assert tree.getEntry_called
    assert 1 == events.iEvent
    assert 11 == tree.ievent

def test_pass_arguments_to_base_class():
    tree = MockTree(entries=1000)
    events = Events(tree, 100)
    assert 100 == events.nEvents
    assert 0 == events.start

    events = Events(tree, 100, 20)
    assert 100 == events.nEvents
    assert 20 == events.start

##__________________________________________________________________||
