#
# SimpleViewer
# Ver 0.1
# Author: Kenny Huang
# Copyright (c) 2017 pointcloud-ai
# https://github.com/pointcloud-ai
#

from threading import Thread, Condition

class ProducerConsumerThread:
    def __init__(self, producer, consumer):
        self.producer = producer
        self.consumer = consumer
        self.running = True

        self.thread = Thread(target= self.consumeFunction)
        self.condition = Condition()
        self.thread.start()

    def produceFunction(self, *args):
        self.condition.acquire()
        self.producer(*args)
        self.condition.notify()
        self.condition.release()

    def consumeFunction(self):
        self.condition.acquire()
        while self.running:
            self.condition.wait(0.25)
            self.consumer()
        self.condition.release()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
