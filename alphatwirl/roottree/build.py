# Tai Sakuma <tai.sakuma@gmail.com>
import logging

import ROOT

from .inspect import is_ROOT_null_pointer

##__________________________________________________________________||
class BuildEvents(object):
    def __init__(self, config):
        self.config = config

    def __repr__(self):
        name_value_pairs = (
            ('config', self.config),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self):
        paths = self.config['file_paths']
        if self.config['check_files']:
            paths = self._verify_files(paths, self.config['skip_error_files'])
        chain = ROOT.TChain(self.config['tree_name'])
        for path in paths:
            chain.Add(path)
        events = self.config['events_class'](
            chain, self.config['max_events'], self.config['start'])
        events.config = self.config
        return events

    def _verify_files(self, paths, skip_error_files):
        ret = [ ]
        for path in paths:
            file_ = ROOT.TFile.Open(path)
            if is_ROOT_null_pointer(file_) or file_.IsZombie():
                logger = logging.getLogger(__name__)
                if skip_error_files:
                    logger.warning('cannot open {}'.format(path))
                    continue
                logger.error('cannot open {}'.format(path))
                raise OSError('cannot open {}'.format(path))
            ret.append(path)
        return ret

##__________________________________________________________________||
