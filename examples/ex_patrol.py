'''
Patrol Model Example
'''

import logging
import time
import random

import collabo


def patrol_func(self):
    if random.randint(1, 100) > self.params['task_rate']:
        return

    sleep_time = round(random.uniform(1.0, 5.0), 1)
    self.logger.info("Processing task for {} sec...".format(sleep_time))
    time.sleep(sleep_time)
    if random.randint(1, 100) <= self.params['failure_rate']:
        raise RuntimeError("cannot finish task")
    self.logger.info("Task done")


if __name__ == "__main__":
    # initialize logger
    import logging_conf
    logger = logging.getLogger('Example')
    mon_logger = logging.getLogger('Monitor')

    # run model
    model = collabo.PatrolModel(logger)
    model.enable_monitor(mon_logger)
    model.name = 'Watcher'
    workers = model.register_workers('Patrol', patrol_func, num=5)
    for worker in workers:
        worker.params = {
            'task_rate': 30,
            'failure_rate': 5
        }
    logger.info("Starting process")
    model.run()
    logger.info("Process finished")
