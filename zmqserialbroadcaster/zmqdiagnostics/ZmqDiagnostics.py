# -*- coding: utf-8 -*-
""" ZMQ message tester """

import zmq
import logging

class ZmqDiagnostics:

    def __init__(self):
        self.port = ""
        self.topic = ""
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self.is_socket_open = False


    def open_zmq(self):
        """
        opens zmq socket for listening
        :return:
        """
        if not self.is_socket_open:
            if self.port != "":
                try:
                    self._socket.bind("tcp://*:" + self.port)
                    self.is_socket_open = True
                except zmq.error.ZMQError as e:
                    logging.error("Could not open zmq socket on port " + self.port)
                    raise e
            else:
                try:
                    self._socket.bind_to_random_port("tcp://*")
                    self.is_socket_open = True
                except zmq.error.ZMQError as e:
                    logging.error("Could not open zmq for listening on random port ")
                    raise e