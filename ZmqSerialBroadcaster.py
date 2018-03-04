#! /bin/env python3
# -*- coding: utf-8 -*-

"""
Module documentation.
"""

# Imports
import sys
# import os
import configparser
# import time
import logging
import zmqserialbroadcaster.serialreader.SerialReader as serialReader
import zmqserialbroadcaster.zmqbroadcaster.ZmqBroadcaster as zmqBroadcaster

# Global variables

serial_reader = serialReader.SerialReader()
zmq_broadcaster = zmqBroadcaster.ZmqBroadcaster()


# Class declarations

# Function declarations

def read_config_file():
    """
    reads config file
    :return:
    """
    config = configparser.ConfigParser()
    config.read('solar.ini')
    serial_reader.device = config['SERIALPORT']['device']
    serial_reader.parity = config['SERIALPORT']['parity']
    serial_reader.databits = config['SERIALPORT']['databits']
    serial_reader.baud = config['SERIALPORT']['baud']
    serial_reader.stop = config['SERIALPORT']['stop']
    zmq_broadcaster.port = config['ZMQ']['port']

def main():
    """
    main thingy
    :return:
    """
    args = sys.argv[1:]

    if not args:
        print('usage: [config file] ')
        sys.exit(1)

    read_config_file()
    try:
        serial_reader.open_port()
    except Exception:
        logging.error("Could not open serial port " + serial_reader.device)
        exit(1)

    while 1:
        serial_reader.read_data()
        zmq_broadcaster.write_data(serial_reader.data)


# Main body
if __name__ == '__main__':
    main()
