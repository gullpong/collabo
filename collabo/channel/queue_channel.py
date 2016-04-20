'''
Queue Channel - Channel Implemented as Queue
'''

# ==============================================================================
# Definition
# ==============================================================================

import threading
import Queue

from channel import Channel


class QueueChannel(Channel):
    def __init__(self, maxsize):
        self.q = Queue.Queue(maxsize=maxsize)

    def size(self):
        return self.q.qsize()

    def clear(self):
        # waste all queued messages
        while self.q.qsize() > 0:
            try:
                self.q.get(True, 1)
            except:
                break

    def send(self, message, block=False, timeout=None):
        # do not send None message
        if message is None:
            return False
        try:
            if block and timeout is None:
                # NOTE: Queue.put() does not respond to interrupt signals
                #       when blocked.
                #       So, it is necessary to use a polling mechanism to avoid
                #       indefinite freezing.
                while True:
                    try:
                        self.q.put(message, block, 1)
                        break
                    except Queue.Full:
                        pass
            else:
                self.q.put(message, block, timeout)
            return True
        except Queue.Full:
            return False

    def receive(self, block=False, timeout=None):
        try:
            if block and timeout is None:
                # NOTE: Queue.get() does not respond to interrupt signals
                #       when blocked.
                #       So, it is necessary to use a polling mechanism to avoid
                #       indefinite freezing.
                while True:
                    try:
                        message = self.q.get(block, 1)
                        break
                    except Queue.Empty:
                        pass
            else:
                message = self.q.get(block, timeout)
            return message
        except Queue.Empty:
            return None
