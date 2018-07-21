# Tai Sakuma <tai.sakuma@gmail.com>
import os
import logging
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from alphatwirl.roottree.inspect import get_entries_in_tree_in_file

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
def test_no_error():
    input_dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_02')
    input_basename = 'sample_chain_02.root'
    path = os.path.join(input_dirname, input_basename)
    tree_name = 'tree'
    assert 1000 == get_entries_in_tree_in_file(path, tree_name)

def test_no_tree(caplog):
    input_dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_02')
    input_basename = 'sample_chain_02.root'
    path = os.path.join(input_dirname, input_basename)
    tree_name = 'no_such_tree'

    with caplog.at_level(logging.WARNING):
        result = get_entries_in_tree_in_file(path, tree_name)

    assert result is None
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'inspect' in caplog.records[0].name
    assert 'cannot find' in caplog.records[0].msg

@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_zombie(caplog):
    input_dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_02')
    input_basename = 'sample_chain_03_zombie.root'
    path = os.path.join(input_dirname, input_basename)
    tree_name = 'tree'

    with caplog.at_level(logging.WARNING):
        result = get_entries_in_tree_in_file(path, tree_name)

    assert result is None
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'inspect' in caplog.records[0].name
    assert 'cannot open' in caplog.records[0].msg

##__________________________________________________________________||
