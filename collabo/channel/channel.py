'''
Channel - Worker-shared Message Queue
'''

# ==============================================================================
# Definition
# ==============================================================================

class Channel(object):
    def __init__(self, maxsize=None):
        # NOTE: Infinite channel size if 'maxsize' is 'None'.
        raise NotImplementedError

    def size(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def send(self, message, block, timeout):
        # NOTE: Generally 'message' should be serializable.
        raise NotImplementedError

    def receive(self, block, timeout):
        # NOTE: This method should return 'None' if no message is in the
        #       channel for the non-blocking mode.
        raise NotImplementedError
