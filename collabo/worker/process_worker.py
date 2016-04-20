'''
Process Worker - Process Implementation of Worker
'''

# ==============================================================================
# Definition
# ==============================================================================

import multiprocessing
import signal
import sys
import os

from worker import Worker


class ProcessWorker(Worker, multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        Worker.__init__(self, *args, **kwargs)
        multiprocessing.Process.__init__(self)

    def kill(self):
        # send a termination signal
        # NOTE: This will raise SystemExit exception by the signal handler.
        #       If the process has a submodel running, the submodel's exception
        #       handler will kill subprocesses in a recursive manner.
        try:
            if sys.platform != 'win32':
                # Unix - send SIGTERM
                os.kill(self.pid, signal.SIGTERM)
            else:
                # Windows - send Ctrl + Break key press (caught by SIGBREAK)
                # NOTE: The problem for Windows is that the signal is sent to
                #       *ALL* processes, making the whole application stop.
                os.kill(self.pid, signal.CTRL_BREAK_EVENT)
        except Exception:
            pass

    def run(self):
        try:
            Worker.run(self)
        except (KeyboardInterrupt, SystemExit):
            # dead from interrupt
            self.change_state('DEAD', 'interrupt')
            # NOTE: Do not handle system interrupts here because they are sent
            #       to all child processes and we want to handle them only in
            #       the root process.
