'''
Demon - Simple Thread Process for Iterative Tasks
'''

# ==============================================================================
# Definition
# ==============================================================================

import threading
import time


class Demon(threading.Thread):
    # interval for polling during sleep
    POLL_INTERVAL = 0.5

    def __init__(
            self,
            task_func, init_func=None, term_func=None,
            head_start=True, iteration=None, interval=1.0):
        threading.Thread.__init__(self)
        self.task_func = task_func
        self.init_func = init_func
        self.term_func = term_func

        self.head_start = head_start
        self.iteration = iteration
        self.interval = interval

        self.daemon = True
        self.stopped = True
        self.quit = False

    @property
    def is_running(self):
        return not self.stopped

    def stop(self):
        self.stopped = True

    def run(self):
        self.stopped = False
        try:
            if self.init_func:
                self.init_func(self)

            iteration_left = self.iteration
            while not self.stopped:
                ts = time.time()

                # if head-start, do task first
                if self.head_start:
                    self.task_func(self)

                # sleep while polling out stop flag
                while not self.stopped:
                    sleep_time = min(
                                self.interval - (time.time() - ts),
                                self.POLL_INTERVAL)
                    if sleep_time <= 0.0:
                        break
                    time.sleep(sleep_time)

                # if not head-start, do task after interval
                if not self.head_start:
                    self.task_func(self)

                # check iteration
                if iteration_left is not None:
                    iteration_left -= 1
                    if iteration_left <= 0:
                        break

            if self.term_func:
                self.term_func(self)

        finally:
            self.stopped = True
