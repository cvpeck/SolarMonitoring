#!./bin/python3
# -*- coding: utf-8 -*-
#
""" Serial device manager """
import serial
import logging
from pylibftdi import Device


class SerialReader:
    """ Class to manage serial devices - ftdi or plain serial """
    def __init__(self):
        self.baud = 9600
        self.bits = 8
        self.parity = "N"
        self.stop = 1
        self.port_open = False
        self.serial_data = ""
        self.device = ""
        # self.serial_connection = ""

    def open_port(self):
        """ Attempts to open port, first as an ftdi device, then as a plain serial device """
        if not self.port_open:
            try:
                # Try opening device as a FTDI identifier
                self.serial_connection = Device(self.device)
                self.serial_connection.open()
                self.port_open = True
                logging.info("Sucessfully opened ftdi device")
            except:
                # TODO actually find out what exception is raised here
                # raise Exception
                logging.warning("Could not open ftdi device")
        if not self.port_open:
            try:
                self.serial_connection = serial.Serial(
                    port=self.device,
                    baudrate=self.baud,
                    parity=self.parity,
                    stopbits=self.stop,
                    bytesize=self.bits,
                    timeout=1
                )
                self.port_open = True
                logging.info("Sucessfully opened plain serial device")
            except serial.serialutil.SerialException:
                # raise Exception
                logging.warning("Could not open serial device")
        if not self.port_open:
            logging.error("Could not open any serial device")
            raise IOError

    def read_data(self):
        """ Read data from already open serial port """
        if self.port_open:
            try:
                self.serial_data = self.serial_connection.readline()
            except:
                # raise Exception
                logging.error("Could not read from serial port")
        else:
            # raise an exception
            logging.error("Attempt to read from closed port")

    def write_data(self, serial_data):
        """ Write data to already open serial port """
        if self.port_open:
            try:
                self.serial_connection.write(serial_data)
            except:
                # raise exception
                logging.error("Attempt to write data to a closed port")