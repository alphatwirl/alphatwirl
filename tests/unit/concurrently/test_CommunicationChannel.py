# Tai Sakuma <tai.sakuma@cern.ch>
import unittest
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
class TestCommunicationChannel(unittest.TestCase):

    def test_repr(self):
        dropbox = MockDropbox()
        obj = CommunicationChannel(dropbox = dropbox)
        repr(obj)

    def test_begin_end(self):
        dropbox = MockDropbox()
        obj = CommunicationChannel(dropbox = dropbox)

        self.assertEqual(0, dropbox.nopened)
        self.assertEqual(0, dropbox.nclosed)

        obj.begin()
        self.assertEqual(1, dropbox.nopened)
        self.assertEqual(0, dropbox.nclosed)

        obj.begin()
        self.assertEqual(1, dropbox.nopened) # don't open twice
        self.assertEqual(0, dropbox.nclosed)

        obj.end()
        self.assertEqual(1, dropbox.nopened)
        self.assertEqual(1, dropbox.nclosed)

        obj.end()
        self.assertEqual(1, dropbox.nopened)
        self.assertEqual(1, dropbox.nclosed) # don't close twice

        obj.begin()
        self.assertEqual(2, dropbox.nopened) # can open again
        self.assertEqual(1, dropbox.nclosed)


    def test_put(self):
        dropbox = MockDropbox()
        obj = CommunicationChannel(dropbox = dropbox)
        obj.begin()

        task1 = MockTask('task1')
        obj.put(task1)

        task2 = MockTask('task2')
        obj.put(task2, 123, 'ABC', A = 34)

        self.assertEqual([
            TaskPackage(task = task1, args = (), kwargs = {}),
            TaskPackage(task = task2, args = (123, 'ABC'), kwargs = {'A': 34}),
        ], dropbox.packages)

        obj.end()

    def test_receive(self):
        dropbox = MockDropbox()
        obj = CommunicationChannel(dropbox = dropbox)
        obj.begin()

        result1 = MockResult('result1')
        dropbox.result = result1
        self.assertEqual(result1, obj.receive())

        obj.end()

    def test_put_when_closed(self):
        dropbox = MockDropbox()
        obj = CommunicationChannel(dropbox = dropbox)

        # logging.getLogger('alphatwirl').setLevel(logging.DEBUG)
        task1 = MockTask('task1')
        obj.put(task1)

        self.assertEqual([ ], dropbox.packages) # empty

    def test_receive_when_closed(self):
        dropbox = MockDropbox()
        obj = CommunicationChannel(dropbox = dropbox)

        # logging.getLogger('alphatwirl').setLevel(logging.DEBUG)
        result1 = MockResult('result1')
        dropbox.result = result1
        self.assertIsNone(obj.receive())

        obj.end()

##__________________________________________________________________||
