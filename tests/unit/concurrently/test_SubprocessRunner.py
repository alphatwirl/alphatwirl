import unittest
import os
import stat
import time
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
class MockWorkingArea(object):
    def open(self):
        self.path = self._prepare_dir()
        self._setup_packages()

    def close(self):
        shutil.rmtree(self.path)
        self.path = None

    def _prepare_dir(self):
        path = tempfile.mkdtemp()
        path_run_py = os.path.join(path, 'run.py')
        with open(path_run_py, 'w') as f:
            f.write(run_py)
        os.chmod(path_run_py, os.stat(path_run_py).st_mode | stat.S_IXUSR)
        return path

    def _setup_packages(self):
        os.makedirs(os.path.join(self.path, 'aaa'))
        os.makedirs(os.path.join(self.path, 'bbb'))
        os.makedirs(os.path.join(self.path, 'ccc'))
        with open(os.path.join(self.path, 'aaa', 'sleep.txt'), 'w') as f:
            f.write('0.20')
        with open(os.path.join(self.path, 'bbb', 'sleep.txt'), 'w') as f:
            f.write('0.02')
        with open(os.path.join(self.path, 'ccc', 'sleep.txt'), 'w') as f:
            f.write('0.15')

        self.package_path_dict = {0:'aaa', 1:'bbb', 2:'ccc'}

    def package_path(self, package_index):
        return self.package_path_dict[package_index]

##__________________________________________________________________||
class TestSubprocessRunner(unittest.TestCase):

    def setUp(self):
        self.workingArea = MockWorkingArea()
        self.workingArea.open()

    def tearDown(self):
        self.workingArea.close()

    def test_run_wait_terminate(self):
        obj = SubprocessRunner(pipe = True)

        pid1 = obj.run(self.workingArea, 0)
        pid2 = obj.run(self.workingArea, 1)
        pid3 = obj.run(self.workingArea, 2)

        self.assertEqual({pid1, pid2, pid3}, set(obj.wait()))
        # obj.wait() returns a list of finished pids, unsorted

        self.assertEqual(
            '{} aaa 0.20'.format(pid1),
            open(os.path.join(self.workingArea.path, 'aaa', 'result.txt')).read()
        )
        self.assertEqual(
            '{} bbb 0.02'.format(pid2),
            open(os.path.join(self.workingArea.path, 'bbb', 'result.txt')).read()
        )
        self.assertEqual(
            '{} ccc 0.15'.format(pid3),
            open(os.path.join(self.workingArea.path, 'ccc', 'result.txt')).read()
        )

        obj.failed_runids([])

        obj.terminate()

    def test_run_poll_terminate(self):
        # don't explicitly test poll() because the finished jobs are
        # not deterministic. poll() is used by wait() and is
        # indirectly tested through wait().
        pass

    def test_run_terminate(self):
        obj = SubprocessRunner(pipe = True)
        pid1 = obj.run(self.workingArea, 0)
        pid2 = obj.run(self.workingArea, 1)
        pid3 = obj.run(self.workingArea, 2)
        obj.terminate()

    def test_wait_terminate(self):
        obj = SubprocessRunner(pipe = True)
        expected = [ ]
        actual = obj.wait()
        self.assertEqual(expected, actual)
        obj.terminate()

##__________________________________________________________________||

