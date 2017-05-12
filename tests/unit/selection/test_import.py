import unittest
import inspect

import alphatwirl

##__________________________________________________________________||

class TestImport(unittest.TestCase):

    def test_functions(self):
        self.assertTrue(inspect.isfunction(alphatwirl.selection.build_selection))

    def test_classes(self):
        self.assertTrue(inspect.isclass(alphatwirl.selection.modules.All))
        self.assertTrue(inspect.isclass(alphatwirl.selection.modules.Any))
        self.assertTrue(inspect.isclass(alphatwirl.selection.modules.Not))
        self.assertTrue(inspect.isclass(alphatwirl.selection.modules.AllwCount))
        self.assertTrue(inspect.isclass(alphatwirl.selection.modules.AnywCount))
        self.assertTrue(inspect.isclass(alphatwirl.selection.modules.NotwCount))

##________________________________._________________________________||
