# Tai Sakuma <tai.sakuma@gmail.com>
import time
import collections


# This file is stored here rather than in tests/ so that it can be
# found by pickle.load()

##__________________________________________________________________||
MockResult = collections.namedtuple('MockResult', 'name args kwargs')

class MockTask(object):
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __call__(self, *args, **kwargs):
        time.sleep(self.time)
        return MockResult(name=self.name, args=args, kwargs=kwargs)

##__________________________________________________________________||
