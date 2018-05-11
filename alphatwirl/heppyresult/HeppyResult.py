# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import os
import re
from .Component import Component
from .ReadVersionInfo import ReadVersionInfo

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
DEFAULT_EXCLUDE_LIST = ['Chunks', 'failed']
DEFAULT_COMPONENT_HAS_THESE_FILES = ['config.pck', 'config.txt']

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class HeppyResult(object):
    """A Heppy result

    Args:
        path (str): the path to the Heppy result
        componentNames (list, optional): the list of the names of the components to read. If not given, all components except the ones listed in `excludeList` will be read.
        excludeList (list, optional): a list of the names of the directory in the Heppy result directory which are to be excluded to be considered as components. if not given, `DEFAULT_EXCLUDE_LIST` will be used.
        componentHasTheseFiles (list, optional): the directories with there files are considered as components. if not given, `DEFAULT_COMPONENT_HAS_THESE_FILES` will be used.
        isComponent (function, optional): a function that determines if a directory is a Heppy component. if not give, `IsComponent` will be used.
    """

    def __init__(self, path,
                 componentNames = None,
                 excludeList = DEFAULT_EXCLUDE_LIST,
                 componentHasTheseFiles = DEFAULT_COMPONENT_HAS_THESE_FILES,
                 isComponent = None,
    ):
        self.path = os.path.normpath(path)
        self.isComponent = IsComponent(excludeList, componentHasTheseFiles) if isComponent is None else isComponent
        allComponentNames = [n for n in os.listdir(self.path) if self.isComponent(os.path.join(self.path, n))]
        allComponentNames = sorted(allComponentNames, key = lambda n: [float(c) if c.isdigit() else c for c in re.findall('\d+|\D+', n)])
        if componentNames is not None:
            nonexistentComponent =  [c for c in componentNames if c not in allComponentNames]
            if len(nonexistentComponent) > 0:
                raise ValueError("No such components: " + ", ".join(nonexistentComponent))
            self.componentNames = componentNames
        else:
            self.componentNames = allComponentNames

        self._compDict = { }
        self._versionInfo = None
        self._readVersionInfo = ReadVersionInfo()

    def __getattr__(self, name):
        if name not in self._compDict:
            if name not in self.componentNames:
                raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
            path = os.path.join(self.path, name)
            self._compDict[name] = Component(path)
        return self._compDict[name]

    def components(self):
        return [getattr(self, n) for n in self.componentNames]

    def versionInfo(self):
        if self._versionInfo is None:
            path = os.path.join(self.path, 'versionInfo.txt')
            self._versionInfo = self._readVersionInfo(path)
        return self._versionInfo

##__________________________________________________________________||
class IsComponent(object):
    def __init__(self, excludeList, componentHasTheseFiles):
        self.excludeList = excludeList
        self.componentHasTheseFiles = componentHasTheseFiles

    def __call__(self, path):
        if not os.path.isdir(path): return False
        if os.path.basename(path) in self.excludeList: return False
        if not set(self.componentHasTheseFiles).issubset(set(os.listdir(path))): return False
        return True

##__________________________________________________________________||
