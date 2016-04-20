'''
Table - Worker-shared Key-value Store
'''

# ==============================================================================
# Definition
# ==============================================================================

class Table(object):
    def __init__(self):
        raise NotImplementedError

    def size(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def access(self):
        # NOTE: This method should be a context manager.
        raise NotImplementedError

    def read(self, key):
        # NOTE: Generally 'key' should be hashable.
        raise NotImplementedError

    def write(self, key, value):
        # NOTE: Generally 'value' should be serializable.
        # NOTE: This method should return the previous 'value' of the 'key'.
        raise NotImplementedError

    def remove(self, key):
        # NOTE: This method should return the previous 'value' of the 'key'.
        raise NotImplementedError
