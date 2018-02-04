# Tai Sakuma <tai.sakuma@gmail.com>
import os
import stat
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import SubprocessRunner

##__________________________________________________________________||
run_py_content = """
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
run_py_content = run_py_content.lstrip()

##__________________________________________________________________||
@pytest.fixture()
def taskdir(tmpdir_factory):
    ret = tmpdir_factory.mktemp('')
    ret = str(ret)
    path_run_py = os.path.join(ret, 'run.py')
    with open(path_run_py, 'w') as f:
        f.write(run_py_content)
        os.chmod(path_run_py, os.stat(path_run_py).st_mode | stat.S_IXUSR)
    return ret

def create_package(taskdir, package_path, sleep_time):
    os.makedirs(os.path.join(taskdir, package_path))
    with open(os.path.join(taskdir, package_path, 'sleep.txt'), 'w') as f:
            f.write(sleep_time)

@pytest.fixture()
def package0(taskdir):
    create_package(taskdir=taskdir, package_path='aaa', sleep_time='0.20')

@pytest.fixture()
def package1(taskdir):
    create_package(taskdir=taskdir, package_path='bbb', sleep_time='0.02')

@pytest.fixture()
def package2(taskdir):
    create_package(taskdir=taskdir, package_path='ccc', sleep_time='0.15')

@pytest.fixture()
def package3(taskdir):
    create_package(taskdir=taskdir, package_path='ddd', sleep_time='100.000')

@pytest.fixture()
def workingarea(taskdir, package0, package1, package2, package3):
    ret = mock.MagicMock(path=taskdir)
    package_path_dict = {0:'aaa', 1:'bbb', 2:'ccc', 3:'ddd'}
    ret.package_path.side_effect = lambda x: package_path_dict[x]
    return ret

def test_mockworkingarea(workingarea):
    assert 'aaa' == workingarea.package_path(0)
    assert 'bbb' == workingarea.package_path(1)
    assert 'ccc' == workingarea.package_path(2)

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return SubprocessRunner()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_run_wait_terminate(obj, workingarea):

    pid1 = obj.run(workingarea, 0)
    pid2 = obj.run(workingarea, 1)
    pid3 = obj.run(workingarea, 2)

    assert {pid1, pid2, pid3} == set(obj.wait())
    # obj.wait() returns a list of finished pids, unsorted

    assert '{} aaa 0.20'.format(pid1) == open(os.path.join(workingarea.path, 'aaa', 'result.txt')).read()
    assert '{} bbb 0.02'.format(pid2) == open(os.path.join(workingarea.path, 'bbb', 'result.txt')).read()
    assert '{} ccc 0.15'.format(pid3) == open(os.path.join(workingarea.path, 'ccc', 'result.txt')).read()

    obj.failed_runids([])

    obj.terminate()

def test_run_poll_terminate(obj, workingarea):
    pid1 = obj.run(workingarea, 0)
    pid2 = obj.run(workingarea, 1)
    pid3 = obj.run(workingarea, 2)
    obj.poll()
    obj.terminate()

def test_run_terminate(obj, workingarea):
    pid1 = obj.run(workingarea, 0)
    pid2 = obj.run(workingarea, 1)
    pid3 = obj.run(workingarea, 2)
    obj.terminate()

def test_wait_terminate(obj):
    assert [ ] == obj.wait()
    obj.terminate()

def test_poll_terminate_long_task(obj, workingarea):
    pid = obj.run(workingarea, 3)
    obj.poll()
    obj.terminate()
    result_path = os.path.join(workingarea.path, 'ddd', 'result.txt')
    assert not os.path.isfile(result_path)

def test_terminate_long_task(obj, workingarea):
    pid = obj.run(workingarea, 3)
    obj.terminate()
    result_path = os.path.join(workingarea.path, 'ddd', 'result.txt')
    assert not os.path.isfile(result_path)

##__________________________________________________________________||
def test_run_multiple_wait_terminate(obj, workingarea):

    pids = obj.run_multiple(workingarea, [0, 1, 2])

    assert set(pids) == set(obj.wait())
    # obj.wait() returns a list of finished pids, unsorted

    assert '{} aaa 0.20'.format(pids[0]) == open(os.path.join(workingarea.path, 'aaa', 'result.txt')).read()
    assert '{} bbb 0.02'.format(pids[1]) == open(os.path.join(workingarea.path, 'bbb', 'result.txt')).read()
    assert '{} ccc 0.15'.format(pids[2]) == open(os.path.join(workingarea.path, 'ccc', 'result.txt')).read()

    obj.failed_runids([])

    obj.terminate()

##__________________________________________________________________||
