'''
Basic Model Example
'''

import logging
import time
import random

import collabo


def worker_func(self):
    delay = random.uniform(1.0, 5.0)
    self.sleep(delay)

    delay = random.uniform(0.1, self.params['task_duration'])
    self.logger.info("Doing task for {}".format(delay))
    time.sleep(delay)
    self.logger.info("Task done")


if __name__ == "__main__":
    # initialize logger
    import logging_conf
    logger = logging.getLogger('Example')
    mon_logger = logging.getLogger('Monitor')

    # run model
    model = collabo.BasicModel(logger)
    model.enable_monitor(mon_logger)
    workers = model.register_workers('Worker', worker_func, num=3)
    for worker in workers:
        worker.params = {
            'task_duration': 5.0,
        }
    logger.info("Starting process")
    model.run()
    logger.info("Process finished")
