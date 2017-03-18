from alphatwirl.configure import TableFileNameComposer
import unittest

##__________________________________________________________________||
class TestTableFileNameComposer(unittest.TestCase):

    def test_one(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, 2)
        )
        self.assertEqual("tbl_n_component_var1_1_var2_var3_2.txt", actual)

    def test_default_prefix(self):
        obj = TableFileNameComposer(default_prefix = 'tbl_Sum')
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, 2)
        )
        self.assertEqual("tbl_Sum_var1_1_var2_var3_2.txt", actual)

    def test_default_suffix(self):
        obj = TableFileNameComposer(default_suffix = '.hdf5')
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, 2)
        )
        self.assertEqual("tbl_n_component_var1_1_var2_var3_2.hdf5", actual)

    def test_empty(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ( ),
            indices = ( )
        )
        self.assertEqual("tbl_n_component.txt", actual)

    def test_star(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, '*')
        )
        self.assertEqual("tbl_n_component_var1_1_var2_var3.txt", actual)

    def test_backref(self):
        obj = TableFileNameComposer()
        actual = obj(
            columnNames = ('var1', 'var2', 'var3', 'var4', 'var5'),
            indices = (1, None, '*', '(*)', '\\1')
        )
        self.assertEqual("tbl_n_component_var1_1_var2_var3_var4_var5.txt", actual)

##__________________________________________________________________||
