#!/usr/bin/env python
import alphatwirl
import unittest

##____________________________________________________________________________||
# How to run test
# at the directory one up (under AlphaTwirl/)
#
# to run all tests in this file
# $ python -m unittest tests.test_test_example
#
# to run a particular test in this file
# $ python -m unittest tests.test_test_example.TestExample1
# 
# to run all tests in all files
# $ python -m unittest discover

##____________________________________________________________________________||
class TestExample1(unittest.TestCase):
    def test_example(self):
        pass
    pass

##____________________________________________________________________________||
class TestExample2(unittest.TestCase):
    def test_example(self):
        pass
    pass

##____________________________________________________________________________||
