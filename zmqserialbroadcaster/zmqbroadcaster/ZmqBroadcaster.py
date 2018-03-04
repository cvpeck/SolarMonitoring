#!./bin/python3
# -*- coding: utf-8 -*-
#
""" ZMQ message broadcaster """

import zmq
import logging


class ZmqBroadcaster:
    """
    ZMQ message broadcaster.
    """
    def __init__(self):
        self.port = ""
        self.topic = ""
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self.is_socket_open = False

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
                    logging.error("Could not open zmq socket on port " + self.port)
                    raise e
            else:
                try:
                    self._socket.bind_to_random_port()
                    self.is_socket_open = True
                except zmq.error.ZMQError as e:
                    logging.error("Could not open zmq on random port ")
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
                logging.error("Fatal zmq error", e)
                raise e
        else:
            if self.topic != "":
                try:
                    self._socket.send_string("%s %s" % (self.topic, messagedata), encoding="utf-8")
                except Exception as e:
                    logging.error("Could not write zmq message to port")
                    raise e
            else:
                logging.error("ZMQ message topic not set")
                raise zmq.error.ZMQError
