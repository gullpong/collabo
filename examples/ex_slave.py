'''
Slave Model Example
'''

import logging
import time
import random

import collabo


def slave_func(self, job):
    sleep_time = round(random.uniform(1.0, 5.0), 1)
    self.logger.info("Processing {} for {} sec...".format(job, sleep_time))
    time.sleep(sleep_time)
    if random.randint(1, 100) <= self.params['failure_rate']:
        raise RuntimeError("cannot finish {}".format(job))
    self.logger.info("{} done".format(job))


def master_func(self):
    self.logger.info("Loading jobs")
    for i in xrange(self.params['job_num']):
        if self.params['check_workers']:
            self.check_workers()
        job = 'JOB-{}'.format(i + 1)
        self.post_job(job)
        self.logger.info("{} loaded".format(job))

    self.logger.info("Releasing workers")
    self.release_workers()


if __name__ == "__main__":
    # initialize logger
    import logging_conf
    logger = logging.getLogger('Example')
    mon_logger = logging.getLogger('Monitor')

    # run model
    model = collabo.SlaveModel(logger)
    model.enable_monitor(mon_logger)
    model.name = 'Master'
    model.params = {
        'job_num': 20,
        'check_workers': True
    }
    workers = model.register_workers('Slave', slave_func, num=5)
    for worker in workers:
        worker.params = {
            'failure_rate': 0
        }
    logger.info("Starting process")
    model.run(master_func)
    logger.info("Process finished")
