import unittest
import sys
import os
import tempfile
import shutil

from alphatwirl.concurrently import HTCondorJobSubmitter

##__________________________________________________________________||
class MockWorkingArea(object):
    def open(self):
        self.path = tempfile.mkdtemp()

    def close(self):
        shutil.rmtree(self.path)
        self.path = None

    def package_path(self, package_index):
        return ''

##__________________________________________________________________||
class MockPopen(object):
    def communicate(self, *args, **kwargs):
        return 'submitted to cluster 1012.', ''

##__________________________________________________________________||
class MockPIPE(object):
    pass

##__________________________________________________________________||
class MockSubprocess(object):
    def __init__(self):
        self.PIPE = MockPIPE

    def Popen(self, *args, **kwargs):
        return MockPopen()

##__________________________________________________________________||
class TestHTCondorJobSubmitter(unittest.TestCase):

    def setUp(self):
        self.module = sys.modules['alphatwirl.concurrently.HTCondorJobSubmitter']
        self.org_subprocess = self.module.subprocess
        self.module.subprocess = MockSubprocess()
        self.cwd = os.getcwd()

        self.workingArea = MockWorkingArea()
        self.workingArea.open()

    def tearDown(self):
        self.module.subprocess = self.org_subprocess
        os.chdir(self.cwd)

        self.workingArea.close()

    def test_run(self):
        obj = HTCondorJobSubmitter()
        ## obj.run(workingArea = self.workingArea, package_index = 0)

##__________________________________________________________________||

