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
    from alphatwirl.roottree import Branch
    from alphatwirl.roottree import BranchBuilder
    from alphatwirl.roottree import BranchAddressManager
    from alphatwirl.roottree import BranchAddressManagerForVector

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
class MockLeaf(object):
    def __init__(self, name, typename):
        self.name = name
        self.typename = typename

    def GetName(self):
        return self.name

    def GetTypeName(self):
        return self.typename

class MockTree(object):
    def __init__(self, *_, **__):
        self.leaf_names = ('run', 'evt', 'njet', 'jet_pt', 'met_pt', 'trigger_path', 'EventAuxiliary')
        self.leaf_type_names = ('Int_t', 'Int_t', 'Int_t', 'Double_t', 'Double_t', 'vector<string>', 'edm::EventAuxiliary')
        self.leafs = dict([(n, MockLeaf(n, t)) for n, t in zip(self.leaf_names, self.leaf_type_names)])

    def SetBranchStatus(self, *_, **__):
        pass

    def GetListOfLeaves(self):
        return self.leafs.values()

    def GetLeaf(self, name):
        return self.leafs[name]

@pytest.fixture()
def mockTree():
    ret = mock.Mock(wraps=MockTree())
    return ret

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def mockBranchAddressManager(monkeypatch):
    ret = mock.Mock(spec=BranchAddressManager)
    def getArrays(tree, branchName):
        leafNames = ('run', 'evt', 'njet', 'jet_pt', 'met_pt')
        if branchName in leafNames:
            return mock.Mock(name=branchName), mock.Mock(name='{}_counter'.format(branchName))
        return None, None
    ret.getArrays.side_effect = getArrays
    module = sys.modules['alphatwirl.roottree.BranchBuilder']
    monkeypatch.setattr(module, 'branchAddressManager', ret)
    yield ret

@pytest.fixture(autouse=True)
def mockBranchAddressManagerForVector(monkeypatch):
    ret = mock.Mock(spec=BranchAddressManagerForVector)
    def getVector(tree, branchName):
        leaf_dict = dict(trigger_path='string')
        if branchName in leaf_dict:
            return mock.Mock(name=branchName, spec=ROOT.vector(leaf_dict[branchName]))
        return None
    ret.getVector.side_effect = getVector
    module = sys.modules['alphatwirl.roottree.BranchBuilder']
    monkeypatch.setattr(module, 'branchAddressManagerForVector', ret)
    yield ret

##__________________________________________________________________||
def test_repr():
    obj = BranchBuilder()
    repr(obj)

def test_register_tree(mockTree):
    obj = BranchBuilder()
    obj.register_tree(mockTree)
    assert [mock.call('*', 0)] == mockTree.SetBranchStatus.call_args_list
    assert mockTree in obj.itsdict

def test_register_tree_two_builders(mockTree):
    obj1 = BranchBuilder()
    obj2 = BranchBuilder()
    obj1.register_tree(mockTree)
    obj2.register_tree(mockTree)
    assert 1 == mockTree.SetBranchStatus.call_count

def test_call_ctypes(mockTree):
    obj = BranchBuilder()
    obj.register_tree(mockTree)
    result = obj(mockTree, 'jet_pt')
    assert isinstance(result, Branch)

def test_call_not_registered(mockTree, caplog):
    obj = BranchBuilder()
    with caplog.at_level(logging.WARNING):
        result = obj(mockTree, 'jet_pt')
    assert isinstance(result, Branch)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'BranchBuilder' in caplog.records[0].name
    assert 'tree is not registered' in caplog.records[0].msg

def test_call_ctypes_same_objects_different_calls(mockTree):
    obj = BranchBuilder()
    obj.register_tree(mockTree)
    result1 = obj(mockTree, 'jet_pt')
    result2 = obj(mockTree, 'jet_pt')
    assert result1 is result2

def test_call_ctypes_same_objects_different_builders(mockTree):
    obj1 = BranchBuilder()
    obj2 = BranchBuilder()
    obj1.register_tree(mockTree)
    obj2.register_tree(mockTree)
    result1 = obj1(mockTree, 'jet_pt')
    result2 = obj2(mockTree, 'jet_pt')
    assert result1 is result2

@pytest.mark.skipif(sys.version_info[0]!=2, reason="skip for Python 3")
def test_call_stdvector(mockTree):
    obj = BranchBuilder()
    obj.register_tree(mockTree)
    result = obj(mockTree, 'trigger_path')
    assert isinstance(result, ROOT.vector('string'))

def test_call_unknown_type(mockTree, caplog):
    obj = BranchBuilder()
    obj.register_tree(mockTree)
    with caplog.at_level(logging.WARNING):
        result = obj(mockTree, 'EventAuxiliary')
    assert result is None
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'BranchBuilder' in caplog.records[0].name
    assert 'unknown leaf type' in caplog.records[0].msg

def test_call_no_such_branch(mockTree):
    obj = BranchBuilder()
    obj.register_tree(mockTree)
    result = obj(mockTree, 'no_such_branch')
    assert result is None

##__________________________________________________________________||
def test_empty_chain(caplog):
    tree_name = 'tree'
    chain = ROOT.TChain(tree_name)
    # add no files to the chain

    obj = BranchBuilder()
    obj.register_tree(chain)

    with caplog.at_level(logging.WARNING):
        assert obj(chain, 'var') is None

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert 'BranchBuilder' in caplog.records[0].name
    assert 'cannot get' in caplog.records[0].msg

##__________________________________________________________________||
