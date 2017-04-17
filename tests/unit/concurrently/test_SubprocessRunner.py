import unittest
import os
import stat
import tempfile
import shutil

from alphatwirl.concurrently import SubprocessRunner

##__________________________________________________________________||
run_py = """
#!/usr/bin/env python
import time
import sys
import os
time.sleep(float(sys.argv[1]))
print os.getpid(),
print ' '.join(sys.argv)
"""
run_py = run_py.lstrip()

##__________________________________________________________________||
class TestSubprocessRunner(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _copy_run_script_to_taskdir(self, content, taskdir):
        path = os.path.join(taskdir, 'run.py')
        f = open(path, 'w')
        f.write(content)
        f.close()
        os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)

    def test_run_wait_terminate(self):
        self._copy_run_script_to_taskdir(run_py, self.tmpdir)
        obj = SubprocessRunner(pipe = True)
        pid1 = obj.run(taskdir = self.tmpdir, package_path = '0.20')
        pid2 = obj.run(taskdir = self.tmpdir, package_path = '0.02')
        pid3 = obj.run(taskdir = self.tmpdir, package_path = '0.15')
        expected = [
            ('{} ./run.py 0.20\n'.format(pid1), ''),
            ('{} ./run.py 0.02\n'.format(pid2), ''),
            ('{} ./run.py 0.15\n'.format(pid3), ''),
        ]
        actual = obj.wait()
        self.assertEqual(expected, actual)
        obj.terminate()

    def test_run_terminate(self):
        self._copy_run_script_to_taskdir(run_py, self.tmpdir)
        obj = SubprocessRunner(pipe = True)
        obj.run(taskdir = self.tmpdir, package_path = '0.20')
        obj.run(taskdir = self.tmpdir, package_path = '0.02')
        obj.run(taskdir = self.tmpdir, package_path = '0.15')
        obj.terminate()

    def test_wait_terminate(self):
        self._copy_run_script_to_taskdir(run_py, self.tmpdir)
        obj = SubprocessRunner(pipe = True)
        expected = [ ]
        actual = obj.wait()
        self.assertEqual(expected, actual)
        obj.terminate()

##__________________________________________________________________||

