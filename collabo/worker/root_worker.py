'''
Root Worker - Dummy Worker for Root Process
'''


# ==============================================================================
# Definition
# ==============================================================================

from worker import Worker


class RootWorker(Worker):
    def __init__(self, table, logger):
        Worker.__init__(self, 'Root', 'Root', table, logger, None)

        # always running
        self.change_state('RUNNING')

    def run(self):
        # not allowed to call
        raise NotImplementedError
