'''
Monitor Demon - Demon for Real-time Monitoring
'''

# ==============================================================================
# Definition
# ==============================================================================

from demon import Demon


class MonitorDemon(Demon):
    def __init__(self, model, logger, interval, mute_threshold):
        Demon.__init__(
                self,
                self.monitor_task, self.monitor_init, self.monitor_term,
                interval=interval, head_start=True)
        self.model = model
        self.logger = logger
        self.mute_threshold = mute_threshold

    @staticmethod
    def monitor_init(self):
        self.muted = False
        self.prev_string = ''
        self.unchanged_time = 0.0

    @staticmethod
    def monitor_task(self):
        # format monitor string
        string = self.model.format_monitor()

        # update monitor string of the parent worker
        self.model.parent.set_info('monitor', string)

        if not self.logger:
            return

        # check if logging needs to be muted
        if self.mute_threshold is not None:
            if string != self.prev_string:
                self.muted = False
                self.unchanged_time = 0.0
            elif not self.muted:
                self.unchanged_time += self.interval
                if self.unchanged_time >= self.mute_threshold:
                    self.muted = True
                    self.logger.info("... ... ...")
        self.prev_string = string

        # log monitor information if not muted
        if not self.muted:
            self.logger.info(string)

    @staticmethod
    def monitor_term(self):
        # clear monitor string of the parent worker
        self.model.parent.set_info('monitor', None)
