# -*- coding: utf-8 -*-
""" Test class for ZmqBroadcaster"""
from unittest import TestCase, main
import pytest
import zmq
import solarlogger.zmqbroadcaster.ZmqBroadcaster as zmqBroadcaster
# import solarlogger.serialreader.SerialReader as serialReader


class TestZmqBroadcaster(TestCase):
    def setUp(self):
        """ Setup routine for testing class. Creates various types of zmq devices to be used by tests """
        self.zmq_broadcaster = zmqBroadcaster.ZmqBroadcaster()
        self.privilidged_port = "76"
        self.in_use_port = "4243"  # Use netstat -anp tcp | grep -i "listen" to pick an in-use non-privilidged course
        self.usual_port = "5678"
        self.topic = "TESTING"
        self.empty_message = ""
        self.normal_message = "This is a normal length test message"

    def test_open_zmq_with_privilidged_port(self):
        """ Test opening the zmq broadcaster on a privilidged port """
        self.zmq_broadcaster.port = self.privilidged_port
        with pytest.raises(zmq.error.ZMQError):
            self.zmq_broadcaster.open_zmq()

    def test_open_zmq_with_in_use_port(self):
        """ Test opening the zmq broadcaster on an in use port """
        self.zmq_broadcaster.port = self.in_use_port
        with pytest.raises(zmq.error.ZMQError):
            self.zmq_broadcaster.open_zmq()

    def test_open_zmq(self):
        """ Test opening the zmq port works correctly"""
        assert not self.zmq_broadcaster.is_socket_open
        self.zmq_broadcaster.port = self.usual_port
        self.zmq_broadcaster.open_zmq()
        assert self.zmq_broadcaster.is_socket_open

    def test_write_data_no_topic_set(self):
        """ Test writing data without setting a topic """
        self.zmq_broadcaster.port = self.usual_port
        self.zmq_broadcaster.open_zmq()
        self.zmq_broadcaster.topic = ""
        with pytest.raises(zmq.ZMQError):
            self.zmq_broadcaster.write_data(self.normal_message)


    def test_write_data(self):
        """ Test opening the zmq broadcaster then write """
        self.zmq_broadcaster.port = self.usual_port
        self.zmq_broadcaster.open_zmq()
        self.zmq_broadcaster.topic = "MyTopic"
        self.zmq_broadcaster.write_data(self.normal_message)

if __name__ == '__main__':
    main()
