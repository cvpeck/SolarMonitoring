# -*- coding: utf-8 -*-
#
""" Solar Logger """
from pprint import pprint
import json
import logging


class DataImporter:

    def __init__(self):
        self.input_file = None
        self._data = None

    def read_from_file(self):
        """ Read json data from file"""
        try:
            self._data = json.load(open(self.input_file))
            pprint(self._data)
        except FileNotFoundError:
            logging.warning("Could not open data file " + self.filename)

    def get_data(self):
        """ Returns data structure"""
        return self._data