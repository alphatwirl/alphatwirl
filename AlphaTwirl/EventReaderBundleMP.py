# Tai Sakuma <sakuma@fnal.gov>
import multiprocessing

##____________________________________________________________________________||
class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, lock):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.lock = lock

    def run(self):
        proc_name = self.name
        while True:
            task = self.task_queue.get()
            if task is None:
                self.task_queue.task_done()
                break
            readers = task()
            self.task_queue.task_done()
            self.result_queue.put(readers)

##____________________________________________________________________________||
class Task(object):
    def __init__(self, eventBuilder, component, readers):
        self.eventBuilder = eventBuilder
        self.component = component
        self.readers = readers

    def __call__(self):
        events = self.eventBuilder.build(self.component)
        for event in events:
            for reader in self.readers:
                reader.event(event)
        return self.readers

##____________________________________________________________________________||
class EventReaderBundleMP(object):

    def __init__(self, eventBuilder, nprocesses = 16):
        self._eventBuilder = eventBuilder
        self._nprocesses = nprocesses
        self._packages = [ ]
        self._readers = { }

    def addReaderPackage(self, package):
        self._packages.append(package)

    def begin(self):
        self._tasks = multiprocessing.JoinableQueue()
        self._results = multiprocessing.Queue()
        self._ntasks = 0
        self._lock = multiprocessing.Lock()

        for i in xrange(self._nprocesses):
            worker = Worker(self._tasks, self._results, self._lock)
            worker.start()

    def read(self, component):

        readers = [ ]
        for package in self._packages:
            reader = package.make(component.name)
            reader.id = id(reader)
            self._readers[id(reader)] = reader
            readers.append(reader)

        task = Task(self._eventBuilder, component, readers)
        self._tasks.put(task)
        self._ntasks += 1

    def end(self):
        for i in xrange(self._nprocesses):
            self._tasks.put(None)
        self._tasks.join()

        for i in xrange(self._ntasks):
            readers = self._results.get()
            for reader in readers:
                self._readers[reader.id].setResults(reader.results())

        for package in self._packages:
            package.collect()

##____________________________________________________________________________||
