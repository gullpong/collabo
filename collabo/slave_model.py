'''
Slave Model - Master Distributing Jobs to Workers
'''


# ==============================================================================
# Definition
# ==============================================================================

# ------------------------------------------------------------------------------
# Formatting Functions
# ------------------------------------------------------------------------------

def format_channel(channel, channel_name, prev_string=''):
    string = prev_string
    if string:
        string += '  '
    string += '{}: {}'.format(channel_name.title(), channel.size())
    return string


# ------------------------------------------------------------------------------
# Worker Task Function Wrapper
# ------------------------------------------------------------------------------

def worker_task_func_wrapper(self):
    if self.init_func:
        self.init_func(self)

    # job handling loop
    while True:
        with self.toggle_state('WAITING', 'job'):
            command, job = self.channel.receive(block=True)
        if command == 'QUIT':
            break
        # NOTE: The received job is passed as an argument to
        #       the job handling function.
        self.job_func(self, job)

    if self.term_func:
        self.term_func(self)


# ------------------------------------------------------------------------------
# Slave Model
# ------------------------------------------------------------------------------

from basic_model import BasicModel
from channel import QueueChannel


class SlaveModel(BasicModel):
    def __init__(
            self, logger,
            channel=None,
            parent=None, suppress_exc=True,
            worker_cls=None, table_cls=None):
        BasicModel.__init__(
                self, logger, parent, suppress_exc,
                worker_cls, table_cls)
        self.channel = channel or QueueChannel(maxsize=100)

    def format_monitor(self):
        string = BasicModel.format_monitor(self)
        string = format_channel(self.channel, 'Jobs', string)
        return string

    def register_workers(
            self, group,
            job_func, init_func=None, term_func=None,
            num=1):
        # create workers while replacing task function with wrapper
        workers = BasicModel.register_workers(
                self, group, worker_task_func_wrapper, num)

        # set worker attributes
        for worker in workers:
            worker.channel = self.channel
            worker.job_func = job_func
            worker.init_func = init_func
            worker.term_func = term_func

        return workers

    def release_workers(self):
        # send quit command for the number of workers
        message = ('QUIT', None)
        with self.parent.toggle_state('BLOCKED', 'channel'):
            for worker in self.workers:
                self.channel.send(message, block=True)

    def post_job(self, job):
        # send job command
        message = ('JOB', job)
        with self.parent.toggle_state('BLOCKED', 'channel'):
            self.channel.send(message, block=True)

    def run(self, task_func=None):
        try:
            BasicModel.run(self, task_func)
        finally:
            self.channel.clear()
