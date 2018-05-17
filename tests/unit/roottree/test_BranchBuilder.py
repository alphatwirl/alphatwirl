# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True


if not has_no_ROOT:
    from alphatwirl.roottree import BranchBuilder

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
class MockFile(object):
    pass

class MockLeaf(object):
    def __init__(self, name, typename):
        self.name = name
        self.typename = typename

    def GetName(self):
        return self.name

    def GetTypeName(self):
        return self.typename

class MockTree(object):
    def __init__(self, Entries = 100):
        self.Entries = Entries
        self.iEvent = -1
        self.branchstatus = [ ]
        self.getEntryCalled = False
        self.leafNames = ('run', 'evt', 'njet', 'jet_pt', 'met_pt', 'trigger_path', 'EventAuxiliary')
        self.leafTypeNames = ('Int_t', 'Int_t', 'Int_t', 'Double_t', 'Double_t', 'vector<string>', 'edm::EventAuxiliary')
        self.leafs = dict([(n, MockLeaf(n, t)) for n, t in zip(self.leafNames, self.leafTypeNames)])

    def GetDirectory(self):
        return MockFile()
    def GetEntries(self):
        return self.Entries
    def GetEntry(self, ientry):
        self.getEntryCalled = True
        if ientry < self.Entries:
            nbytes = 10
            self.iEvent = ientry
        else:
            nbytes = 0
            self.iEvent = -1
        return nbytes

    def SetBranchStatus(self, bname, status):
        self.branchstatus.append((bname, status))

    def GetListOfLeaves(self):
        return self.leafs.values()

    def GetLeaf(self, name):
        return self.leafs[name]

def test_mocktree():
    tree = MockTree(Entries=3)
    assert isinstance(tree.GetDirectory(), MockFile)
    assert 3 == tree.GetEntries()

    assert -1 == tree.iEvent

    nbytes = 10
    assert nbytes == tree.GetEntry(0)
    assert 0 == tree.iEvent
    assert nbytes == tree.GetEntry(1)
    assert 1 == tree.iEvent
    assert nbytes == tree.GetEntry(2)
    assert 2 == tree.iEvent
    assert 0 == tree.GetEntry(3)
    assert -1 == tree.iEvent

##__________________________________________________________________||
class MockArray(object):
    pass

class MockBranchAddressManager(object):
    def __init__(self):
        self.leafNames = ('run', 'evt', 'njet', 'jet_pt', 'met_pt')
    def getArrays(self, tree, branchName):
        if branchName in self.leafNames:
            return MockArray(), MockArray()
        return None, None

class MockVector(object): pass

class MockBranchAddressManagerForVector(object):
    def __init__(self):
        self.leafNames = ('trigger_path', )
    def getVector(self, tree, branchName):
        if branchName in self.leafNames:
            return MockVector()
        return None

class MockBranch(object):
    def __init__(self, name, array, countarray):
        pass

@pytest.fixture(autouse=True)
def branch_address_manager(monkeypatch):
    ret = MockBranchAddressManager()
    module = sys.modules['alphatwirl.roottree.BranchBuilder']
    monkeypatch.setattr(module, 'branchAddressManager', ret)
    yield ret

@pytest.fixture(autouse=True)
def branch_address_manager_for_vector(monkeypatch):
    ret = MockBranchAddressManagerForVector()
    module = sys.modules['alphatwirl.roottree.BranchBuilder']
    monkeypatch.setattr(module, 'branchAddressManagerForVector', ret)
    yield ret

@pytest.fixture(autouse=True)
def mock_branch(monkeypatch):
    module = sys.modules['alphatwirl.roottree.BranchBuilder']
    monkeypatch.setattr(module, 'Branch', MockBranch)
    yield

@pytest.fixture(autouse=True)
def clear_dict():
    yield
    BranchBuilder.itsdict.clear()

##__________________________________________________________________||
def test_init():
    obj = BranchBuilder()

def test_repr():
    obj = BranchBuilder()
    repr(obj)

def test_getattr():
    obj = BranchBuilder()
    tree = MockTree()

    jet_pt = obj(tree, 'jet_pt')
    met_pt = obj(tree, 'met_pt')
    assert isinstance(jet_pt, MockBranch)
    assert isinstance(met_pt, MockBranch)

def test_getattr_same_objects_different_calls():
    obj = BranchBuilder()

    tree = MockTree()
    jet_pt1 = obj(tree, 'jet_pt')
    met_pt1 = obj(tree, 'met_pt')

    jet_pt2 = obj(tree, 'jet_pt')
    met_pt2 = obj(tree, 'met_pt')

    assert jet_pt1 is jet_pt2
    assert met_pt1 is met_pt2

def test_getattr_same_objects_different_builders():

    obj1 = BranchBuilder()
    obj2 = BranchBuilder()

    tree = MockTree()
    jet_pt1 = obj1(tree, "jet_pt")
    met_pt1 = obj1(tree, "met_pt")

    jet_pt2 = obj2(tree, "jet_pt")
    met_pt2 = obj2(tree, "met_pt")

    assert jet_pt1 is jet_pt2
    assert met_pt1 is met_pt2

def test_getattr_None():
    obj = BranchBuilder()
    tree = MockTree()
    assert obj(tree, 'no_such_branch') is None

def test_getattr_warning(caplog):
    obj = BranchBuilder()
    tree = MockTree()
    with caplog.at_level(logging.WARNING):
        assert obj(tree, 'EventAuxiliary') is None

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert 'BranchBuilder' in caplog.records[0].name
    assert 'tree is not registered' in caplog.records[0].msg

def test_register_tree():
    obj = BranchBuilder()
    tree = MockTree()
    obj.register_tree(tree)
    assert [('*', 0)] == tree.branchstatus
##__________________________________________________________________||
