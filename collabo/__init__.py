'''
Collabo - Framework for Multi-task Workers

Jinyong Lee (gullpong9@gmail.com)
'''

# ==============================================================================
# Import
# ==============================================================================

from basic_model import BasicModel
from slave_model import SlaveModel
from patrol_model import PatrolModel


# ==============================================================================
# Initialization
# ==============================================================================

import signal
import sys


# NOTE: Handle SIGTERM/SIGBREAK so that it raises SystemExit exception instead
#       abruptly aborting the process.
#       In this way, we can guarantee all clean-up procedures are executed
#       properly (e.g., releasing locks) especially when workers are
#       force-stopped.
#       This routine runs only once for each process at the moment
#       collabo package is imported.
def _sigterm_handler(signum, frame):
    raise SystemExit
if sys.platform != 'win32':
    # Unix - catch SIGTERM
    signal.signal(signal.SIGTERM, _sigterm_handler)
else:
    # Windows - catch SIGBREAK
    signal.signal(signal.SIGBREAK, _sigterm_handler)
