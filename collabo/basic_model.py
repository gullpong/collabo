'''
Basic Model - Workers Doing Tasks
'''

# ==============================================================================
# Definition
# ==============================================================================

# ------------------------------------------------------------------------------
# Formatting Functions
# ------------------------------------------------------------------------------

STATUS_CODE = {
    'BORN':     '*',
    'DEAD':     '-',
    'RUNNING':  'R',
    'BLOCKED':  'B',
    'WAITING':  'W',
    'SLEEPING': 'z',
}

def format_state(state, prev_string=''):
    string = prev_string
    if state['status'] in STATUS_CODE:
        st_code = STATUS_CODE[state['status']]
    else:
        st_code = state['status'][0].upper()
    if state['detail']:
        st_desc = state['detail'][0].lower()
    else:
        st_desc = '.'
    string += ' {}{}'.format(st_code, st_desc)
    return string

def format_workers(workers, prev_string=''):
    string = prev_string

    # grouping workers with their group names
    groups = {}
    for worker in workers:
        if worker.group not in groups:
            groups[worker.group] = []
        groups[worker.group].append(worker)

    # format grouped worker's state and monitor information
    for group, workers in groups.items():
        if string:
            string += '  '
        string += '{}:'.format(group.title())
        for worker in workers:
            string = format_state(worker.state, string)
            monitor = worker.get_info('monitor')
            if monitor:
                string += ' {{ {} }}'.format(monitor)

    return string


# ------------------------------------------------------------------------------
# Basic Model
# ------------------------------------------------------------------------------

from worker import ThreadWorker
from worker import RootWorker
from table import DictTable
from demon import MonitorDemon


class BasicModel(object):
    def __init__(
            self, logger,
            parent=None, suppress_exc=True,
            worker_cls=None, table_cls=None):
        self.name = 'Main'
        self.logger = logger
        self.parent = parent
        self.suppress_exc = suppress_exc

        self.worker_cls = worker_cls or ThreadWorker
        self.table_cls = table_cls or DictTable

        if not self.parent:
            self.parent = RootWorker(self.table_cls(), self.logger)

        self.workers = []
        self.mon_demon = None

    @property
    def is_root(self):
        return isinstance(self.parent, RootWorker)

    def register_workers(self, group, task_func, num=1):
        workers = []
        for i in xrange(num):
            # set label
            if num > 1:
                label = '{}_{:02}'.format(group.title(), i + 1)
            else:
                label = group.title()
            # create worker instance
            worker = self.worker_cls(
                    group, label,
                    self.table_cls(),
                    self.logger.getChild(label),
                    task_func)
            workers.append(worker)
            self.workers.append(worker)
        return workers

    def start_workers(self):
        for worker in self.workers:
            worker.start()

    def wait_workers(self):
        for worker in self.workers:
            worker.join()

    def stop_workers(self):
        for worker in self.workers:
            worker.kill()

    def check_workers(self):
        for worker in self.workers:
            if worker.state['status'] == 'DEAD':
                raise RuntimeError("worker terminated unexpectedly")

    def format_monitor(self):
        if self.is_root:
            # NOTE: Format parent worker's state when it's root
            #       because it cannot be captured in the worker hierarchy.
            string = '{}:'.format(self.name.title())
            string = format_state(self.parent.state, string)
        else:
            string = ''
        string = format_workers(self.workers, string)
        return string

    def enable_monitor(self, logger=None, interval=1.0, mute_threshold=None):
        self.mon_demon = MonitorDemon(self, logger, interval, mute_threshold)

    def sleep(self, duration, cause=''):
        self.parent.sleep(duration, cause)

    def run(self, task_func=None):
        self.parent.submodel = self
        # start monitor demon if available
        if self.mon_demon:
            self.mon_demon.start()
        try:
            with self.parent.toggle_state('RUNNING', 'model'):
                self.logger.debug("Starting Workers")
                self.start_workers()

                # do task if given
                if task_func:
                    task_func(self)

                self.logger.debug("Waiting for Workers")
                self.wait_workers()

        except (SystemExit, KeyboardInterrupt):
            if self.is_root:
                # NOTE: Log system interrupts only when it is the root process
                #       because they are sent to all child processes.
                self.logger.critical(
                        "Interruption signal received",
                        exc_info=1)
            self.stop_workers()
            if not self.suppress_exc:
                raise

        except Exception:
            self.logger.critical(
                    "Unexpected exception occurred",
                    exc_info=1)
            self.stop_workers()
            if not self.suppress_exc:
                raise

        finally:
            self.parent.submodel = None
            # stop monitor demon if started
            if self.mon_demon:
                self.mon_demon.stop()

