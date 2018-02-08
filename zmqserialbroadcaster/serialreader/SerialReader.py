import serial
import logging
from pylibftdi import Device

class SerialReader:

    def __init__(self):
        self.baud = 9600
        self.bits = 8
        self.parity = "N"
        self.stop = 1
        self.port_open = False


    def open_port(self):
        if not self.port_open :
            try:
                # Try opening device as a FTDI identifier
                self.serial_connection = device(self.device)
                device.open()
                self.port_open = True
                logging.info("Sucessfully opened ftdi device")
            except:
                # raise Exception
                logging.warning("Could not open ftdi device")
        if not self.port_open :
            try:
                self.serial_connection = serial.Serial(
                    port=self.device,
                    baudrate=self.baud,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )
                self.port_open = True
                logging.info("Sucessfully opened plain serial device")
            except serial.serialutil.SerialException:
                # raise Exception
                logging.warning("Could not open serial device")
        if not self.port_open :
            logging.error("Could not open any serial device")
            raise IOError

    def read_data(self):
        self.serial_data = self.serial_connection.readline()
