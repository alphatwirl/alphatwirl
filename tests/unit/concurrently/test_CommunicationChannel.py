# Tai Sakuma <tai.sakuma@gmail.com>
import collections
import logging

from alphatwirl.concurrently import CommunicationChannel, TaskPackage

##__________________________________________________________________||
MockTask = collections.namedtuple('MockTask', 'name')
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
class MockDropbox(object):
    def __init__(self):
        self.nopened = 0
        self.nclosed = 0
        self.packages = [ ]
        self.result = None

    def open(self):
        self.nopened += 1

    def put(self, package):
        self.packages.append(package)

    def receive(self):
        return self.result

    def close(self):
        self.nclosed += 1

##__________________________________________________________________||
class MockProgressReporter(object): pass

##__________________________________________________________________||
class MockProgressMonitor(object):
    def __init__(self):
        self.reporters = [ ]

    def createReporter(self):
        reporter = MockProgressReporter()
        self.reporters.append(reporter)
        return reporter

##__________________________________________________________________||
def test_repr():
    dropbox = MockDropbox()
    obj = CommunicationChannel(dropbox = dropbox)
    repr(obj)

def test_begin_end():
    dropbox = MockDropbox()
    obj = CommunicationChannel(dropbox = dropbox)

    assert 0 == dropbox.nopened
    assert 0 == dropbox.nclosed

    obj.begin()
    assert 1 == dropbox.nopened
    assert 0 == dropbox.nclosed

    obj.begin()
    assert 1 == dropbox.nopened # don't open twice
    assert 0 == dropbox.nclosed

    obj.end()
    assert 1 == dropbox.nopened
    assert 1 == dropbox.nclosed

    obj.end()
    assert 1 == dropbox.nopened
    assert 1 == dropbox.nclosed # don't close twice

    obj.begin()
    assert 2 == dropbox.nopened # can open again
    assert 1 == dropbox.nclosed


def test_put():
    dropbox = MockDropbox()
    obj = CommunicationChannel(dropbox = dropbox)
    obj.begin()

    task1 = MockTask('task1')
    obj.put(task1)

    task2 = MockTask('task2')
    obj.put(task2, 123, 'ABC', A = 34)

    assert [
        TaskPackage(task = task1, args = (), kwargs = {}),
        TaskPackage(task = task2, args = (123, 'ABC'), kwargs = {'A': 34}),
    ] == dropbox.packages

    obj.end()

def test_receive():
    dropbox = MockDropbox()
    obj = CommunicationChannel(dropbox = dropbox)
    obj.begin()

    result1 = MockResult('result1')
    dropbox.result = result1
    assert result1 == obj.receive()

    obj.end()

def test_put_when_closed():
    dropbox = MockDropbox()
    obj = CommunicationChannel(dropbox = dropbox)

    # logging.getLogger('alphatwirl').setLevel(logging.DEBUG)
    task1 = MockTask('task1')
    obj.put(task1)

    assert [ ] == dropbox.packages # empty

def test_receive_when_closed():
    dropbox = MockDropbox()
    obj = CommunicationChannel(dropbox = dropbox)

    # logging.getLogger('alphatwirl').setLevel(logging.DEBUG)
    result1 = MockResult('result1')
    dropbox.result = result1
    assert obj.receive() is None

    obj.end()

##__________________________________________________________________||
