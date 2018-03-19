#!./bin/python3
# -*- coding: utf-8 -*-
#
""" Serial device manager """
import serial
import logging
import json
import threading
import queue
from pylibftdi import Device
from pylibftdi import FtdiError


class SerialReader:
    """ Class to manage serial devices - ftdi or plain serial """
    def __init__(self):
        self.baud = 9600
        self.bits = 8
        self.parity = "N"
        self.stop = 1
        self.is_port_open = False
        self.raw_data = None
        self.device = None
        self.serial_connection = None
        self.json_format = None
        self.json_data = None
        logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)
        self.logger = logging.getLogger(__name__)
        self.data_queue = queue.Queue()
        self.producer_thread = None

    def open_port(self):
        """ Attempts to open port, first as an ftdi device, then as a plain serial device """
        if not self.is_port_open:
            try:
                # Try opening device as a FTDI identifier
                self.serial_connection = Device(self.device)
                self.serial_connection.open()
                self.is_port_open = True
                self.logger.info("Sucessfully opened ftdi device")
            except FtdiError:
                self.logger.warning("Could not open ftdi device")
        if not self.is_port_open:
            try:
                self.serial_connection = serial.Serial(
                    port=self.device,
                    baudrate=self.baud,
                    parity=self.parity,
                    stopbits=self.stop,
                    bytesize=self.bits,
                    timeout=1
                )
                self.is_port_open = True
                self.logger.info("Successfully opened plain serial device")
            except serial.serialutil.SerialException:
                # raise Exception
                self.logger.warning("Could not open serial device")
        if not self.is_port_open:
            self.logger.error("Could not open any serial device")
            raise IOError

    def close_port(self):
        """ Closes the serial port if it is open"""
        if self.is_port_open:
            try:
                self.serial_connection.close()
            except:
                self.logger.warning("Attempt to close port that is not open")
            self.is_port_open = False

    def read_data(self):
        """ Read data from already open serial port """

        if self.is_port_open:
            try:
                self.raw_data = self.serial_connection.readline()
            except:
                # raise Exception
                self.logger.error("Could not read from serial port")
        else:
            # raise an exception
            self.logger.error("Attempt to read from closed port")

    def write_data(self, serial_data):
        """ Write data to already open serial port """
        if self.is_port_open:
            try:
                self.serial_connection.write(serial_data)
            except:
                # raise exception
                self.logger.error("Attempt to write data to a closed port")

    def format_data(self):
        if self.json_data:
            split_line = self.raw_data.split(' ')
            i = 0
            for raw_data in split_line:
                self.logger.debug('raw data - %s', raw_data)
                json_item = json.encode(self.json_format[i], raw_data)
                self.logger.debug('encoded data - %s', json_item)

    def start_thread(self):
        self.producer_thread = ProducerThread(name='serial_producer_of_data', queue=self.data_queue, instance=self)
        self.producer_thread.start()


class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, queue=None, instance=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name
        self.queue = queue
        self.instance = instance

    def run(self):
        while True:
            if not self.queue.full():
                item = self.instance.read_data()
                self.queue.put(item)
                logging.debug('Putting ' + str(item)
                              + ' : ' + str(queue.qsize()) + ' items in queue')
        return
