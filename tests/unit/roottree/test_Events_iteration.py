# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

from alphatwirl.roottree import Events

if not has_no_ROOT:
    from alphatwirl.roottree import BEvents as BEvents


##__________________________________________________________________||
events_classes = [Events]
if not has_no_ROOT:
    events_classes.append(BEvents)
events_classes_ids = [c.__name__ for c in events_classes]

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
@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_init(Events):
    tree = MockTree()
    events = Events(tree)
    events = Events(tree, 100)
    assert tree is events.tree

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_repr(Events):
    tree = MockTree()
    events = Events(tree)
    repr(events)

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_nEvents_default(Events):
    tree = MockTree(entries=100)
    events = Events(tree)
    assert 100 == events.nEvents # default the same as entries
    assert 100 == len(events)

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
@pytest.mark.parametrize('maxEvents, expected ', [
    pytest.param(-1, 100, id='default'),
    pytest.param(50, 50, id='less'),
    pytest.param(120, 100, id='more'),
    pytest.param(100, 100, id='exact'),
])
def test_nEvents(Events, maxEvents, expected):
    tree = MockTree(entries=100)
    events = Events(tree, maxEvents)
    assert expected == events.nEvents
    assert expected == len(events)

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
@pytest.mark.parametrize('maxEvents, start, expected ', [
    pytest.param(-1, 1, 99, id='all_events_start_2nd'),
    pytest.param(10, 1, 10, id='nEvents_equal_maxEvents'),
    pytest.param(-1, 99, 1, id='all_events_start_last'),
    pytest.param(20, 99, 1, id='nEvents_less_than_maxEvents'),
    pytest.param(-1, 100, 0, id='nEvents_zero_1'),
    pytest.param(-1, 110, 0, id='nEvents_zero_2'),
    pytest.param(10, 100, 0, id='nEvents_zero_3'),
])
def test_nEvents_start(Events, maxEvents, start, expected):
    tree = MockTree(entries=100)
    events = Events(tree, maxEvents=maxEvents, start=start)
    assert expected == events.nEvents
    assert expected == len(events)

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_nEvents_start_raise(Events):
    tree = MockTree(entries=100)
    with pytest.raises(ValueError):
        Events(tree, maxEvents=-1, start=-10)

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_iter_iEvent(Events):

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

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_iter_maxEvents(Events):
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

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_iter_iEvent_start(Events):
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

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_iter_maxEvents_start(Events):

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

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_getitem(Events):
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

@pytest.mark.parametrize('Events', events_classes, ids=events_classes_ids)
def test_getitem_start(Events):
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
