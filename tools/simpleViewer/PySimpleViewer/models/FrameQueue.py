#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from DataQueue import DataQueue
from collections import deque

class FrameQueue(DataQueue):
    def __init__(self, maxlen = 3):
        super(FrameQueue, self).__init__(maxlen)
        self.availableQueue = deque(maxlen= maxlen)

    def _put(self, item):
        if len(self.availableQueue) == 0:
            self.queue.append(item.copy())
        else:
            it = self.availableQueue.popleft()
            item.copyTo(it)
            self.queue.append(it)

    def release(self, item):
        self.condition.acquire()
        self.availableQueue.append(item)
        self.condition.release()