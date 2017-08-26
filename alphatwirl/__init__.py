
##__________________________________________________________________||
try:
    ## https://root-forum.cern.ch/t/pyroot-hijacks-help/15207
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    pass

##__________________________________________________________________||

from . import binning
from . import collector
from . import concurrently
from . import configure
from . import roottree
from . import selection
from . import heppyresult
from . import loop
from . import progressbar
from . import summary
from . import delphes
from . import cmsedm
from .misc import mkdir_p
from .misc import list_to_aligned_text
from .misc import quote_string

# to be deleted
from .misc import listToAlignedText

##__________________________________________________________________||
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR) # DEBUG INFO WARN ERROR CRITICAL
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

##__________________________________________________________________||
