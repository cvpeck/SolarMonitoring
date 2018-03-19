#! /bin/env python3
# -*- coding: utf-8 -*-

"""
Module documentation.
"""

# Imports
import sys
import configparser
import pprint
from threading import Thread
import logging
import queue

import solarlogger.serialreader.SerialReader as serialReader
import solarlogger.zmqbroadcaster.ZmqBroadcaster as zmqBroadcaster
import solarlogger.zmqlistener.ZmqListener as zmqListener
import solarlogger.dataimporter.DataImporter as dataImporter
import solarlogger.zmqdiagnostics.ZmqDiagnostics as zmqDiagnostics


# Global variables
BUF_SIZE = 1024
serial_data_queue = queue.Queue(BUF_SIZE)
serial_reader = serialReader.SerialReader()
zmq_broadcaster = zmqBroadcaster.ZmqBroadcaster()
zmq_listener = zmqListener.ZmqListener()
zmq_diagnostics = zmqDiagnostics.ZmqDiagnostics()
data_importer = dataImporter.DataImporter()
json_format = [
            'Date',
            'DailyRunTime',
            'OperatingState',
            'GeneratorVoltage',
            'GeneratorCurrent',
            'GeneratorPower',
            'LineVoltage',
            'LineCurrentFeedIn',
            'PowerFedIn',
            'UnitTemperature'
            ]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def startup_zmq_diagnostics():
    """
    Creates a zmq listener thread that subscribes to all topics
    :return:
    """
    zmq_diagnostics.port = zmq_broadcaster.port
    zmq_diagnostics.open_zmq()
    thread = Thread(target=zmq_diagnostics.display_zmq_messages, args=[])
    thread.start()


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
    zmq_broadcaster.topic = config['ZMQ']['topic']
    zmq_broadcaster.broadcaster = config['ZMQ']['broadcaster']
    zmq_listener.broadcaster = config['ZMQ']['broadcaster']
    zmq_listener.topic = config['ZMQ']['topic']

    data_importer.input_json_file = config['SOLAR']['input_json_file']
    data_importer.input_csv_file = config['SOLAR']['input_csv_file']


def startup_zmq_broadcaster():
    """
    Starts up the zmq broadcaster
    :return:
    """
    zmq_broadcaster.data_queue = serial_data_queue
    zmq_broadcaster.open_zmq()
    zmq_broadcaster.start_thread()

def startup_zmq_listener():
    """
    Starts up the zmq listener
    :return:
    """
    zmq_listener.open_zmq()
    thread = Thread(target=zmq_listener.receive_zmq_messages(), args=[])
    thread.start()

def load_existing_data():
    """
    Loads existing data from csv and json files
    :return:
    """
    data_importer.json_format = json_format
    # loads data from csv file
    imported_data = data_importer.read_from_csv_file()
    for entry in imported_data:
        zmq_broadcaster.write_data(entry)
    # loads data from json file
    # print(json.dumps(data))
#    for entry in data_importer.read_from_json_file():
#        zmq_broadcaster.write_data(entry)


def startup_serial_data():
    """
    Starts thread for reading serial data and broadcasting via zmq
    :return:
    """
    serial_reader.data_queue = serial_data_queue

    try:
        serial_reader.open_port()
    except Exception:
        logger.error("Could not open serial port " + serial_reader.device)
        exit(1)
    serial_reader.json_format = json_format
    # thread = Thread(target=read_serial_data(), args=[])
    # thread.start()
    serial_reader.start_thread()

# def read_serial_data():
#     """
#     Starts reading serial data and broadcasting via zmq
#     :return: Never returns
#     """
#     # TODO replace wit queue startups
#     while 1:
#         serial_reader.read_data()
#         zmq_broadcaster.write_data(serial_reader.json_data)


def main():
    """
    Main function for starting up software
    :return:
    """
    args = sys.argv[1:]

    if not args:
        print('usage: [config file] ')
        sys.exit(1)
    logger.info('Startup of Solar Logging system')
    read_config_file()
    startup_zmq_broadcaster()
#    startup_zmq_diagnostics()
    load_existing_data()
#   startup_serial_data()
    startup_zmq_listener()
#   startup_service_uploader


# Main body
if __name__ == '__main__':
    main()
