#! /bin/env python3
# -*- coding: utf-8 -*-

"""
Module documentation.
"""

# Imports
import sys
import configparser
import logging
import pprint
from threading import Thread

import zmqserialbroadcaster.serialreader.SerialReader as serialReader
import zmqserialbroadcaster.zmqbroadcaster.ZmqBroadcaster as zmqBroadcaster
import zmqserialbroadcaster.dataimporter.DataImporter as dataImporter

import zmqserialbroadcaster.zmqdiagnostics.ZmqDiagnostics as zmqDiagnostics


# Global variables

serial_reader = serialReader.SerialReader()
zmq_broadcaster = zmqBroadcaster.ZmqBroadcaster()
zmq_diagnostics = zmqDiagnostics.ZmqDiagnostics()
data_importer = dataImporter.DataImporter()


# Class declarations

# Function declarations

def activate_zmq_diagnostics():
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
    # TODO add defaults
    # zmq_broadcaster.port = config['ZMQ']['port']
    data_importer.input_json_file = config['SOLAR']['input_json_file']
    data_importer.input_csv_file = config['SOLAR']['input_csv_file']


def startup_zmq():
    zmq_broadcaster.topic = '10001'
    zmq_broadcaster.open_zmq()
    activate_zmq_diagnostics()


def load_existing_data():
    data_importer.json_format = [
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
    # loads data from csv file
    imported_data = data_importer.read_from_csv_file()
    for entry in imported_data:
        zmq_broadcaster.write_data(entry)
    # loads data from json file
     #print(json.dumps(data))
#    for entry in data_importer.read_from_json_file():
#        zmq_broadcaster.write_data(entry)


def load_serial_data():
    try:
        serial_reader.open_port()
    except Exception:
        logging.error("Could not open serial port " + serial_reader.device)
        exit(1)

        serial_reader.json_format = [
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

    while 1:
        serial_reader.read_data()
        zmq_broadcaster.write_data(serial_reader.json_data)


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
    startup_zmq()
    load_existing_data()
#   load_serial_data()



# Main body
if __name__ == '__main__':
    main()
