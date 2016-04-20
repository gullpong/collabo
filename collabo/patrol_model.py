'''
Patrol Model - Workers Handling Routinely Jobs
'''


# ==============================================================================
# Definition
# ==============================================================================

# ------------------------------------------------------------------------------
# Worker Task Function Wrapper
# ------------------------------------------------------------------------------

import time


def worker_task_func_wrapper(self):
    if self.init_func:
        self.init_func(self)

    # job handling loop
    while True:
        ts = time.time()
        self.job_func(self)
        # sleep only when job handling took less than interval
        sleep_time = self.interval - (time.time() - ts)
        if sleep_time > 0.0:
            self.sleep(sleep_time)

    if self.term_func:
        self.term_func(self)


# ------------------------------------------------------------------------------
# Main Task Function Wrapper
# ------------------------------------------------------------------------------

def main_task_func_wrapper(self):
    # main task loop
    while True:
        # verify all workers are runnig fine
        self.check_workers()

        ts = time.time()
        if self.task_func:
            self.task_func(self)

        # sleep only when job handling took less than interval
        sleep_time = self.interval - (time.time() - ts)
        if sleep_time > 0.0:
            self.sleep(sleep_time)


# ------------------------------------------------------------------------------
# Patrol Model
# ------------------------------------------------------------------------------

from basic_model import BasicModel


class PatrolModel(BasicModel):
    def register_workers(
            self, group,
            job_func, init_func=None, term_func=None, interval=1.0,
            num=1):
        # create workers while replacing task function with wrapper
        workers = BasicModel.register_workers(
                self, group, worker_task_func_wrapper, num)

        # set task attributes
        for worker in workers:
            worker.job_func = job_func
            worker.init_func = init_func
            worker.term_func = term_func
            worker.interval = interval

        return workers

    def run(self, task_func=None, interval=1.0):
        # set task attributes
        self.task_func = task_func
        self.interval = interval

        # run model while replacing task function with wrapper
        BasicModel.run(self, main_task_func_wrapper)

