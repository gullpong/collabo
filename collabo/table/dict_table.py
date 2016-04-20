'''
Dictionary Table - Table Implemented as Dictionary
'''

# ==============================================================================
# Definition
# ==============================================================================

import threading
import contextlib
import copy

from table import Table


class DictTable(Table):
    def __init__(self):
        self.lock = threading.Lock()
        self.map = {}

    def size(self):
        with self.access() as table:
            return len(table)

    def clear(self):
        with self.access() as table:
            table.clear()

    @contextlib.contextmanager
    def access(self):
        try:
            # NOTE: lock.acquire() needs to be inside the try-finally block
            #       in order to prevent freezing that can happen when exception
            #       occurs right after the lock is acquired.
            #       In this case, the process exits the function without
            #       releasing the lock.
            self.lock.acquire()

            # pass the access to the internal key-value map
            yield self.map

        finally:
            try:
                self.lock.release()
            except:
                # suppress exceptions from too many releases
                # NOTE: Exception can occur even before lock is fully acquired,
                #       and trying to release it can lead to an exception.
                pass

    def read(self, key):
        with self.access() as table:
            return copy.deepcopy(table.get(key))

    def write(self, key, value):
        with self.access() as table:
            prev_value = table.get(key)
            table[key] = value
        return prev_value

    def remove(self, key):
        with self.access() as table:
            prev_value = table.pop(key, None)
        return prev_value
