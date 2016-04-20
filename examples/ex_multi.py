'''
Multi-level Example
'''

import logging
import time
import random

import collabo


def worker_func(self):
    delay = random.uniform(1.0, 5.0)
    self.sleep(delay)

    delay = random.uniform(0.1, 1.0)
    self.logger.info("Doing task for {}".format(delay))
    time.sleep(delay)
    self.logger.info("Task done")


def spawner_func(self):
    if self.params['spawn_depth'] > 1:
        spawner_num = random.randrange(1, self.params['child_num'])
        worker_num = self.params['child_num'] - spawner_num
    else:
        spawner_num = 0
        worker_num = self.params['child_num']

    delay = random.uniform(1.0, 2.0)
    self.sleep(delay)

    self.logger.info("Spawning children: {} spawners, {} workers".format(
            spawner_num, worker_num))

    model = collabo.BasicModel(self.logger, parent=self)
    model.enable_monitor()
    workers = model.register_workers('Worker', worker_func, num=worker_num)
    spawners = model.register_workers('Spawner', spawner_func, num=spawner_num)
    for spawner in spawners:
        spawner.params = {
            'spawn_depth': self.params['spawn_depth'] - 1,
            'child_num': self.params['child_num'],
        }
    self.logger.info("Starting children")
    model.run()
    self.logger.info("Children finished")


if __name__ == "__main__":
    # initialize logger
    import logging_conf
    logger = logging.getLogger('Example')
    mon_logger = logging.getLogger('Monitor')

    # run model
    model = collabo.BasicModel(logger)
    model.enable_monitor(mon_logger)
    spawners = model.register_workers('Mother', spawner_func, num=1)
    for spawner in spawners:
        spawner.params = {
            'spawn_depth': 3,
            'child_num': 5
        }
    logger.info("Starting process")
    model.run()
    logger.info("Process finished")
