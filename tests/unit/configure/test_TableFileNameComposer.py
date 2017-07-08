from alphatwirl.configure import TableFileNameComposer
import unittest

##__________________________________________________________________||
class TestTableFileNameComposer(unittest.TestCase):

    def test_no_indices(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
        )
        self.assertEqual("tbl_n.var1.var2.var3.txt", actual)

    def test_simple(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, 2)
        )
        self.assertEqual("tbl_n.var1-1.var2.var3-2.txt", actual)

    def test_default_prefix(self):
        obj = TableFileNameComposer(default_prefix = 'tbl_Sum')
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, 2)
        )
        self.assertEqual("tbl_Sum.var1-1.var2.var3-2.txt", actual)

    def test_default_suffix(self):
        obj = TableFileNameComposer(default_suffix = 'hdf5')
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, 2)
        )
        self.assertEqual("tbl_n.var1-1.var2.var3-2.hdf5", actual)

    def test_empty(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ( ),
            indices = ( )
        )
        self.assertEqual("tbl_n.txt", actual)

    def test_star(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, '*')
        )
        self.assertEqual("tbl_n.var1-1.var2.var3-w.txt", actual)

    def test_backref(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ('var1', 'var2', 'var3', 'var4', 'var5'),
            indices = (1, None, '*', '(*)', '\\1')
        )
        self.assertEqual("tbl_n.var1-1.var2.var3-w.var4-wp.var5-b1.txt", actual)

##__________________________________________________________________||
