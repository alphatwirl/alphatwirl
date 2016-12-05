# Tai Sakuma <tai.sakuma@cern.ch>
from .WorkingArea import WorkingArea

##__________________________________________________________________||
class TaskPackageDropbox(object):
    def __init__(self, dispatcher, path, put_alphatwirl = True, user_modules = ()):
        self.dispatcher = dispatcher
        self.path = path
        self.python_modules = list(user_modules)
        if put_alphatwirl: self.python_modules.append('AlphaTwirl')

    def open(self):
        self.workingArea = WorkingArea(self.path)
        self.workingArea.put_python_modules(self.python_modules)
        self.package_indices = [ ]

    def put(self, package):
        package_index, package_path = self.workingArea.put_package(package)
        self.package_indices.append(package_index)
        self.dispatcher.run(self.workingArea.dirpath, package_path)

    def receive(self):
        self.dispatcher.wait()
        results = [self.workingArea.collect_result(i) for i in self.package_indices]
        self.package_indices[:] = [ ]
        return results

    def close(self):
        self.dispatcher.terminate()

##__________________________________________________________________||
