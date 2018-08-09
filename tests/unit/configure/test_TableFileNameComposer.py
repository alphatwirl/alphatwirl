# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.configure import TableFileNameComposer

##__________________________________________________________________||
@pytest.mark.parametrize('init_arg, call_arg, expected', [
    pytest.param(
        { }, dict(columnNames=('var1', 'var2', 'var3')),
        'tbl_n.var1.var2.var3.txt',
        id='no-indices'),
    pytest.param(
        { },
        dict(
            columnNames=('var1', 'var2', 'var3'),
            indices=(1, None, 2)
        ),
        'tbl_n.var1-1.var2.var3-2.txt',
        id='simple'),
    pytest.param(
        dict(default_prefix='tbl_Sum'),
        dict(
            columnNames=('var1', 'var2', 'var3'),
            indices=(1, None, 2)
        ),
        'tbl_Sum.var1-1.var2.var3-2.txt',
        id='default-prefix'),
    pytest.param(
        dict(default_suffix='hdf5'),
        dict(
            columnNames=('var1', 'var2', 'var3'),
            indices=(1, None, 2)
        ),
        'tbl_n.var1-1.var2.var3-2.hdf5',
        id='default-suffix'),
    pytest.param(
        dict(), dict(columnNames=( ), indices=( )), 'tbl_n.txt',
        id='empty'),
    pytest.param(
        dict(), dict(
            columnNames=('var1', 'var2', 'var3'),
            indices=(1, None, '*')
        ),
        'tbl_n.var1-1.var2.var3-w.txt',
        id='star'),
    pytest.param(
        dict(), dict(
            columnNames=('var1', 'var2', 'var3', 'var4', 'var5'),
            indices=(1, None, '*', '(*)', '\\1')
        ),
        'tbl_n.var1-1.var2.var3-w.var4-wp.var5-b1.txt',
        id='backref'),
    pytest.param(
        dict(default_var_separator='#'), dict(
            columnNames=('var1', 'var2', 'var3', 'var4', 'var5'),
            indices=(1, None, '*', '(*)', '\\1')
        ),
        'tbl_n#var1-1#var2#var3-w#var4-wp#var5-b1.txt',
        id='default-var-separator'),
    pytest.param(
        dict(default_idx_separator='#'), dict(
            columnNames=('var1', 'var2', 'var3', 'var4', 'var5'),
            indices=(1, None, '*', '(*)', '\\1')
        ),
        'tbl_n.var1#1.var2.var3#w.var4#wp.var5#b1.txt',
        id='default-idx-separator'),
])
def test_complete(init_arg, call_arg, expected):
    obj = TableFileNameComposer(**init_arg)
    actual = obj(**call_arg)
    assert expected == actual

##__________________________________________________________________||
