from AlphaTwirl.Configure import TableFileNameComposer
import unittest

##__________________________________________________________________||
class TestTableFileNameComposer(unittest.TestCase):

    def test_one(self):
        compose = TableFileNameComposer()
        actual = compose(
            columnNames = ('var1', 'var2', 'var3'),
            indices = (1, None, 2)
        )
        self.assertEqual("tbl_component_var1_1_var2_var3_2.txt", actual)

    def test_empty(self):
        compose = TableFileNameComposer()
        actual = compose(
            columnNames = ( ),
            indices = ( )
        )
        self.assertEqual("tbl_component.txt", actual)

##__________________________________________________________________||
