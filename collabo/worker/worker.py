'''
Worker - Task Procedure Unit
'''


# ==============================================================================
# Definition
# ==============================================================================

import uuid
import time
import contextlib


class Worker(object):
    def __init__(self, group, label, table, logger, task_func):
        self.uid = uuid.uuid4().hex
        self.group = group
        self.label = label
        self.info = table   # use Table for storing worker information
        self.logger = logger
        self.task_func = task_func

        self.submodel = None

        # just born
        self.change_state('BORN')

    @property
    def state(self):
        return self.info.read('state')

    def change_state(self, status, detail=''):
        return self.info.write('state', dict(status=status, detail=detail))

    @contextlib.contextmanager
    def toggle_state(self, status, detail=''):
        prev_state = self.change_state(status, detail)
        try:
            yield prev_state
        finally:
            self.change_state(**prev_state)

    def get_info(self, key):
        return self.info.read(key)

    def set_info(self, key, value):
        if value is None:
            return self.info.remove(key)
        else:
            return self.info.write(key, value)

    def sleep(self, duration, cause=''):
        with self.toggle_state('SLEEPING', cause):
            time.sleep(duration)

    def kill(self):
        raise NotImplementedError

    def run(self):
        try:
            self.change_state('RUNNING')
            self.logger.debug("Started")

            # do task
            self.task_func(self)

            self.change_state('DEAD')
            self.logger.debug("Finished")

        except Exception:
            # dead from error
            self.change_state('DEAD', 'error')
            self.logger.exception("Aborted by unexpected exception")
