import aggregate
import binning
import collector
import concurrently
import configure
import events
import heppyresult
import loop
import progressbar
import summary
from misc import mkdir_p
from misc import listToAlignedText
from misc import quote_string

##__________________________________________________________________||
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR) # DEBUG INFO WARN ERROR CRITICAL
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

##__________________________________________________________________||
try:
    ## https://root-forum.cern.ch/t/pyroot-hijacks-help/15207
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    pass

##__________________________________________________________________||
