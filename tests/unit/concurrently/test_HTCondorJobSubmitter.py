import unittest
import sys
import os
import tempfile
import shutil
import textwrap

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
        self.returncode = 0
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
default_job_desc_template = """
Executable = {job_script}
output = {out}
error = {error}
log = {log}
{args}
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = {input_files}
transfer_output_files = {output_files}
Universe = vanilla
notification = Error
# Initialdir = {initialdir}
getenv = True
queue 1
"""
default_job_desc_template = textwrap.dedent(default_job_desc_template).strip()

##__________________________________________________________________||
job_desc_template_with_extra = """
Executable = {job_script}
output = {out}
error = {error}
log = {log}
{args}
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = {input_files}
transfer_output_files = {output_files}
Universe = vanilla
notification = Error
# Initialdir = {initialdir}
getenv = True
request_memory = 900
queue 1
"""
job_desc_template_with_extra = textwrap.dedent(job_desc_template_with_extra).strip()

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

    def test_init_job_desc_extra(self):
        job_desc_extra = ['request_memory = 900']
        obj = HTCondorJobSubmitter(job_desc_extra = job_desc_extra)
        self.assertEqual(job_desc_template_with_extra, obj.job_desc_template)

    def test_run(self):
        obj = HTCondorJobSubmitter()
        obj.run(workingArea = self.workingArea, package_index = 0)

##__________________________________________________________________||

