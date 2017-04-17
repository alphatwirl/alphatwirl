import unittest
import sys
import os
import tempfile
import shutil

from alphatwirl.concurrently import HTCondorJobSubmitter

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

        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        self.module.subprocess = self.org_subprocess
        os.chdir(self.cwd)

        shutil.rmtree(self.tmpdir)

    def test_run(self):
        obj = HTCondorJobSubmitter()
        obj.run(taskdir = self.tmpdir, package_path = '0.20')

##__________________________________________________________________||

