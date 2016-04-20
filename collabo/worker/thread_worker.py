'''
Thread Worker - Thread Implementation of Worker
'''

# ==============================================================================
# Definition
# ==============================================================================

import threading

from worker import Worker


class ThreadWorker(Worker, threading.Thread):
    def __init__(self, *args, **kwargs):
        Worker.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)
        self.tid = None
        self.killed = False

        # NOTE: Make it as a daemon thread because it is not possible to kill
        #       a thread externally in Python. In this way, terminating the
        #       root process automatically terminates child threads as well.
        self.daemon = True

    def kill(self):
        # NOTE: A thread cannot be killed. We just flag it as killed here.
        self.killed = True
        if self.submodel:
            # recursively kill all child workers
            # NOTE: This has to be done here because there is no possible way
            #       for sending terminating signals to child threads.
            for subworker in self.submodel.workers:
                subworker.kill()

    def join(self, timeout=None):
        if self.killed:
            return
        # NOTE: For a thread, join() does not respond to interrupt signals.
        #       So, it is necessary to use a polling mechanism to avoid
        #       indefinite freezing.
        while True:
            if timeout is not None:
                if not timeout:
                    break
                if timeout > 0.5:
                    join_time = 0.5
                    timeout -= 0.5
                else:
                    join_time = timeout
                    timeout = 0.0
            else:
                join_time = 0.5
            threading.Thread.join(self, join_time)
            if not self.isAlive():
                break

    def run(self):
        # set thread ID
        self.tid = self._Thread__ident
        try:
            Worker.run(self)
        finally:
            # invalidate thread ID
            self.tid = None
