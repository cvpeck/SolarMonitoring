# -*- coding: utf-8 -*-
""" ZMQ message tester """

import zmq
import logging
from pprint import pprint


class ZmqDiagnostics:

    def __init__(self):
        self.port = ''
        self.zmq_publisher_address = '127.0.0.1'
        self.topic = ''  # An empty string will subscribe to all topics
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self.is_socket_open = False
        self.received_topic = None
        self.received_data = None

    def open_zmq(self):
        """
        opens zmq socket for listening
        :return:
        """
        if not self.is_socket_open:
            if self.port == '':
                logging.error('ZMQ Diagnostics port to listen to has not been defined')
            else:
                try:
                    self._socket.connect('tcp://%s:%s' % (self.zmq_publisher_address, self.port))
                    self._socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
                    self.is_socket_open = True
                except zmq.error.ZMQError as e:
                    logging.error("Could connect to  " + self.zmq_publisher_address + self.port)
                    raise e

    def display_zmq_messages(self):
        """
        Displays zmq messages from subscription in a continually running loop
        :return:
        """
        logging.debug('ZMQ Diagnostic listening to tcp://%s:%s' % (self.zmq_publisher_address, self.port))
        while True:
            string = self._socket.recv().decode('utf-8')
            # pprint (string.split())
            self.received_topic, self.received_data = string.split('{')
            logging.debug('Received ZMQ topic: %s message: %s' % (self.received_topic, self.received_data))
