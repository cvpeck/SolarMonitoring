import serial
import logging
from pylibftdi import Device

class SerialReader:

    def __init__(self):
        self.device = "/dev/ttyUSB0"
        self.baud = 9600
        self.bits = 8
        self.parity = "N"
        self.stop = 1
	device = Device('A7022SP5')

    def open_port(self):
        try:
            self.serial_connection = serial.Serial(
                port=self.device,
                baudrate=self.baud,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        except serial.serialutil.SerialException:
            raise Exception

    def read_data(self):
        self.serial_data = self.serial_connection.readline()