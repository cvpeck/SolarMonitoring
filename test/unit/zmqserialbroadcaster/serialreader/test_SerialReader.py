#!./bin/python3
# -*- coding: utf-8 -*-
#
""" SerialReader test routines """

from unittest import TestCase, main
import pytest
import zmqserialbroadcaster.serialreader.SerialReader as serialReader

TEST_FTDI = False
#TEST_FTDI = True


class TestSerialReader(TestCase):
    """ Test class for SerialReader """
    ftdi_connected = pytest.mark.skipif(TEST_FTDI == False,
                                        reason="FTDI cable required for test")
    def setUp(self):
        """ Setup routine for testing class. Creates various types of serial devices to be used by tests """
        """ Use lib ftdi tools to find appropriate correct device for testing and use """
        """ Mac example - system_profiler SPUSBDataType | grep -C 7 FTDI """
        self.serial_ftdi_device = serialReader.SerialReader()
        self.serial_ftdi_device.device = "FT0K3AEM"
        self.serial_plain_device = serialReader.SerialReader()
        self.serial_plain_device.device = "/dev/usb3"
        self.serial_reader_dodgy_device = serialReader.SerialReader()

    def test_object_cannot_be_created_without_device(self):
        with pytest.raises(IOError):
            self.serial_reader_dodgy_device.open_port()

    def test_object_cannot_be_created_wth_non_serial_device(self):
        self.serial_reader_no_device = "/dev/null"
        with pytest.raises(IOError):
            self.serial_reader_dodgy_device.open_port()

    def test_object_cannot_be_created_wth_non_existant_serial_device(self):
        self.serial_reader_no_device = "/dev/bogus"
        with pytest.raises(IOError):
            self.serial_reader_dodgy_device.open_port()

    @ftdi_connected
    def test_open_port(self):
        self.serial_ftdi_device.open_port()
        assert self.serial_ftdi_device.is_port_open
        # self.fail()
        # pass

    @ftdi_connected
    def test_close_port(self):
        self.serial_ftdi_device.open_port()
        self.serial_ftdi_device.close_port()
        assert not self.serial_ftdi_device.is_port_open

    def test_close_already_closed_port(self):
        self.serial_ftdi_device.close_port()
        self.serial_ftdi_device.close_port()
        assert not self.serial_ftdi_device.is_port_open


if __name__ == '__main__':
    main()
