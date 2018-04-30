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
        self.log_level = logging.DEBUG
        logging.basicConfig(level=self.log_level, format='(%(threadName)-9s) %(message)s',)
        self.logger = logging.getLogger(__name__)
        self.data_queue = queue.Queue()
        self.consumer_thread = None

    def set_log_level(self, level):
        self.logger.setLevel(level)


    def add_data(self, data):
        self.logger.debug('Received to add to queue - %s' % data)
        self.data_queue.put(data)

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
                self.logger.debug("Sending zmq message to port %s %s" % (self.topic, messagedata))
                self._socket.send_string("%s %s" % (self.topic, messagedata), encoding="utf-8")
            except Exception as e:
                self.logger.error("Could not write zmq message to port")
                raise e
        else:
            self.logger.error("ZMQ message topic not set")
            raise zmq.error.ZMQError

    def start_thread(self):
        self.consumer_thread = ConsumerThread(name='consumer_of_data_producer_of_zmq_messages', queue=self.data_queue, instance=self)
        self.consumer_thread.start()

    def stop_thread(self):
        self.logger.debug("Thread shutdown")
        self.consumer_thread.stop()

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
        self.instance.logger.info('ZMQ Broadcaster transmitting on port %s' % self.instance.port)
        while True:
            if not self.queue.empty():
                # Removes an item from the queue, blocking until one available
                try:
                    item = self.queue.get_nowait()
                    self.instance.write_data(item)
                    self.instance.logger.debug('Items still in queue - %d' % self.queue.qsize())
                except QueueEmpty:


        return
