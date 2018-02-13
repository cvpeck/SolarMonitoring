#!./bin/python3
# -*- coding: utf-8 -*-
#
""" SerialReader test routines """

import unittest
from serialreader import SerialReader


class TestSerialReader(unittest.TestCase):
    """ Test class for SerialReader """
    def setUp(self):
        """ Setup routine for testing class. Creates various types of serial devices to be used by tests """
        self.serial_ftdi_device = SerialReader
        self.serial_ftdi_device.device = "A7022SP5"
        self.serial_plain_device = SerialReader
        self.serial_plain_device.device = "/dev/usb3"
        self.serial_reader_dodgy_device = SerialReader

    def test_object_cannot_be_created_without_device(self):
        # TODO change to correct error type
        self.assertRaises(IOError, self.serial_reader_dodgy_device.open_port())

    def test_object_cannot_be_created_wth_non_serial_device(self):
        self.serial_reader_no_device = "/dev/null"
        # TODO change to correct error type
        self.assertRaises(IOError, self.serial_reader_dodgy_device.open_port())

    def test_object_cannot_be_created_wth_non_existant_serial_device(self):
        self.serial_reader_no_device = "/dev/bogus"
        # TODO change to correct error type
        self.assertRaises(IOError, self.serial_reader_dodgy_device.open_port())


if __name__ == '__main__':
    unittest.main()
