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
with open(os.path.join(sys.argv[1], 'sleep.txt'), 'r') as f:
    secs = f.read()
time.sleep(float(secs))
with open(os.path.join(sys.argv[1], 'result.txt'), 'w') as f:
    f.write('{} {} {}'.format(os.getpid(), sys.argv[1], secs))
"""
run_py = run_py.lstrip()

##__________________________________________________________________||
class TestSubprocessRunner(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._copy_run_script_to_taskdir(run_py, self.tmpdir)
        self._setup_packages(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _copy_run_script_to_taskdir(self, content, taskdir):
        path = os.path.join(taskdir, 'run.py')
        with open(path, 'w') as f:
            f.write(content)
        os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)

    def _setup_packages(self, taskdir):
        os.makedirs(os.path.join(taskdir, 'aaa'))
        os.makedirs(os.path.join(taskdir, 'bbb'))
        os.makedirs(os.path.join(taskdir, 'ccc'))
        with open(os.path.join(taskdir, 'aaa', 'sleep.txt'), 'w') as f:
            f.write('0.20')
        with open(os.path.join(taskdir, 'bbb', 'sleep.txt'), 'w') as f:
            f.write('0.02')
        with open(os.path.join(taskdir, 'ccc', 'sleep.txt'), 'w') as f:
            f.write('0.15')

    def test_run_wait_terminate(self):
        obj = SubprocessRunner(pipe = True)

        pid1 = obj.run(taskdir = self.tmpdir, package_path = 'aaa')
        pid2 = obj.run(taskdir = self.tmpdir, package_path = 'bbb')
        pid3 = obj.run(taskdir = self.tmpdir, package_path = 'ccc')
        expected = [pid1, pid2, pid3]

        actual = obj.wait()
        self.assertEqual(expected, actual)

        self.assertEqual(
            '{} aaa 0.20'.format(pid1),
            open(os.path.join(self.tmpdir, 'aaa', 'result.txt')).read()
        )
        self.assertEqual(
            '{} bbb 0.02'.format(pid2),
            open(os.path.join(self.tmpdir, 'bbb', 'result.txt')).read()
        )
        self.assertEqual(
            '{} ccc 0.15'.format(pid3),
            open(os.path.join(self.tmpdir, 'ccc', 'result.txt')).read()
        )

        obj.terminate()

    def test_run_terminate(self):
        obj = SubprocessRunner(pipe = True)
        obj.run(taskdir = self.tmpdir, package_path = '0.20')
        obj.run(taskdir = self.tmpdir, package_path = '0.02')
        obj.run(taskdir = self.tmpdir, package_path = '0.15')
        obj.terminate()

    def test_wait_terminate(self):
        obj = SubprocessRunner(pipe = True)
        expected = [ ]
        actual = obj.wait()
        self.assertEqual(expected, actual)
        obj.terminate()

##__________________________________________________________________||

