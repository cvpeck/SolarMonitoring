#!./bin/python3
# -*- coding: utf-8 -*-
#
""" ZMQ message broadcaster """

import zmq
import logging
import threading
import queue


class ZmqBroadcaster:
    """
    ZMQ message broadcaster.
    """
    def __init__(self):
        self.port = ''
        self.topic = ''
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self.is_socket_open = False
        logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)
        self.logger = logging.getLogger(__name__)
        self.data_queue = queue.Queue()
        self.consumer_thread = None

    def open_zmq(self):
        """
        opens zmq socket
        :return:
        """
        if not self.is_socket_open:
            if self.port != "":
                try:
                    self._socket.bind("tcp://*:" + self.port)
                    self.is_socket_open = True
                except zmq.error.ZMQError as e:
                    self.logger.error("Could not open zmq socket on port " + self.port)
                    raise e
            else:
                try:
                    self.port = self._socket.bind_to_random_port("tcp://*")
                    self.is_socket_open = True
                except zmq.error.ZMQError as e:
                    self.logger.error("Could not open zmq on random port ")
                    raise e

    def write_data(self, messagedata):
        """
        write data to zmq socket
        :return:
        """
        if not self.is_socket_open:
            try:
                self.open_zmq()
            except zmq.error.ZMQError as e:
                self.logger.error("Fatal zmq error", e)
                raise e

        if self.topic != "":
            try:
                self._socket.send_string("%s %s" % (self.topic, messagedata), encoding="utf-8")
            except Exception as e:
                self.logger.error("Could not write zmq message to port")
                raise e
        else:
            self.logger.error("ZMQ message topic not set")
            raise zmq.error.ZMQError

    def start_thread(self):
        self.consumer_thread = ConsumerThread(name='zmq_consumer_of_data', queue=self.data_queue, instance=self)
        self.consumer_thread.start()


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, queue=None, instance=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        self.queue = queue
        self.instance = instance
        return

    def run(self):
        while True:
            if not self.queue.empty():
                item = self.queue.get()
                self.instance.write_data(item)
        return
