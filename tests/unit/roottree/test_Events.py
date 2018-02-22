# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.roottree import Events

##__________________________________________________________________||
class MockFile(object):
    pass

##__________________________________________________________________||
class MockTree(object):
    def __init__(self, entries=100):
        self.entries = entries
        self.ievent = -1
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
def test_init():
    tree = MockTree()
    events = Events(tree)
    events = Events(tree, 100)

    assert tree is events.tree

def test_repr():
    tree = MockTree()
    events = Events(tree)
    repr(events)

def test_nEvents():
    tree = MockTree(entries=100)
    events = Events(tree)
    assert 100 == events.nEvents # default the same as entries
    assert 100 == len(events)

    events = Events(tree, -1)
    assert 100 == events.nEvents # the same as entries
    assert 100 == len(events)

    events = Events(tree, 50)
    assert 50 == events.nEvents
    assert 50 == len(events)

    events = Events(tree, 120)
    assert 100 == events.nEvents
    assert 100 == len(events)

    events = Events(tree, 100)
    assert 100 == events.nEvents
    assert 100 == len(events)


def test_nEvents_start():

    tree = MockTree(entries=100)

    events = Events(tree, maxEvents=-1, start=1)
    assert 99 == events.nEvents
    assert 99 == len(events)

    events = Events(tree, maxEvents=10, start=1)
    assert 10 == events.nEvents
    assert 10 == len(events)

    events = Events(tree, maxEvents=-1, start=99)
    assert 1 == events.nEvents
    assert 1 == len(events)

    events = Events(tree, maxEvents=20, start=99)
    assert 1 == events.nEvents
    assert 1 == len(events)

    events = Events(tree, maxEvents=-1, start=100)
    assert 0 == events.nEvents
    assert 0 == len(events)

    events = Events(tree, maxEvents=-1, start=110)
    assert 0 == events.nEvents
    assert 0 == len(events)

    events = Events(tree, maxEvents=10, start=110)
    assert 0 == events.nEvents
    assert 0 == len(events)

    with pytest.raises(ValueError):
        Events(tree, maxEvents=-1, start=-10)


def test_iter_iEvent():

    tree = MockTree(entries=4)
    events = Events(tree)
    assert -1 == events.iEvent

    it = iter(events)
    event = next(it)
    assert 0 == event.iEvent
    assert 0 == tree.ievent
    event = next(it)
    assert 1 == event.iEvent
    assert 1 == tree.ievent
    event = next(it)
    assert 2 == event.iEvent
    assert 2 == tree.ievent
    event = next(it)
    assert 3 == event.iEvent
    assert 3 == tree.ievent
    with pytest.raises(StopIteration):
        next(it)
    assert -1 == event.iEvent


def test_iter_maxEvents():
    tree = MockTree(entries=40)
    events = Events(tree, maxEvents=4)
    assert -1 == events.iEvent

    it = iter(events)
    event = next(it)
    assert 0 == event.iEvent
    event = next(it)
    assert 1 == event.iEvent
    event = next(it)
    assert 2 == event.iEvent
    event = next(it)
    assert 3 == event.iEvent
    with pytest.raises(StopIteration):
        next(it)
    assert -1 == event.iEvent


def test_iter_iEvent_start():
    tree = MockTree(entries=4)
    events = Events(tree, start=2)
    assert -1 == events.iEvent

    it = iter(events)
    event = next(it)
    assert 0 == event.iEvent
    assert 2 == tree.ievent
    event = next(it)
    assert 1 == event.iEvent
    assert 3 == tree.ievent
    with pytest.raises(StopIteration):
        next(it)
    assert -1 ==event.iEvent


def test_iter_maxEvents_start():

    tree = MockTree(entries=40)
    events = Events(tree, maxEvents=4, start=2)
    assert -1 == events.iEvent

    it = iter(events)
    event = next(it)
    assert 0 == event.iEvent
    assert 2 == tree.ievent
    event = next(it)
    assert 1 == event.iEvent
    assert 3 == tree.ievent
    event = next(it)
    assert 2 == event.iEvent
    assert 4 == tree.ievent
    event = next(it)
    assert 3 == event.iEvent
    assert 5 == tree.ievent
    with pytest.raises(StopIteration):
        next(it)
    assert -1 == event.iEvent

def test_iter_getattr():
    tree = MockTree(entries=5)
    events = Events(tree)
    it = iter(events)
    event = next(it)
    assert 1111 == event.branch1
    tree.branch1 = 2222
    assert 2222 == event.branch1

def test_getitem():
    tree = MockTree(entries=4)
    events = Events(tree)
    assert -1 == events.iEvent

    event = events[0]
    assert 0 == event.iEvent
    assert 0 == tree.ievent
    event = events[1]
    assert 1 == event.iEvent
    assert 1 == tree.ievent
    event = events[2]
    assert 2 == event.iEvent
    assert 2 == tree.ievent
    event = events[3]
    assert 3 == event.iEvent
    assert 3 == tree.ievent
    with pytest.raises(IndexError):
        events[4]
    assert -1 == events.iEvent

def test_getitem_start():
    tree = MockTree(entries=4)
    events = Events(tree, start=2)
    assert -1 == events.iEvent

    event = events[0]
    assert 0 == event.iEvent
    assert 2 == tree.ievent
    event = events[1]
    assert 1 == event.iEvent
    assert 3 == tree.ievent
    with pytest.raises(IndexError):
        events[4]
    assert -1 == events.iEvent

##__________________________________________________________________||
