#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from collections import deque
from threading import Condition

import numpy as np

class DataQueue(object):

    def __init__(self, maxlen = 3):
        self.queue = deque(maxlen= maxlen)
        self.maxlen = maxlen
        self.condition = Condition()

    def _put(self, item):
        self.queue.append(item)

    def put(self, item):
        self.condition.acquire()
        self._put(item)
        self.condition.notify()
        self.condition.release()

    def _get(self):
        return self.queue.popleft()

    def get(self, timeout = None):
        self.condition.acquire()
        while not len(self.queue):
            self.condition.wait(timeout)
            if timeout is not None and not len(self.queue):
                self.condition.release()
                return None

        item = self._get()
        self.condition.release()
        return item

    def tryGet(self):
        self.condition.acquire()

        if len(self.queue):
            item = self._get()
        else:
            item = None
        self.condition.release()

        return item
    def clear(self):
        self.queue.clear()