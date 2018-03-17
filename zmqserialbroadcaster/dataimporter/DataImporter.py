# -*- coding: utf-8 -*-
#
""" Solar Logger """
from pprint import pprint
import json
import logging
import csv


class DataImporter:
    """
    Imports data from csv or json files
    """

    def __init__(self):
        self.input_json_file = None
        self.input_csv_file = None
        self.json_data = []
        self._raw_data =[]
        self.json_format = None

    def read_from_json_file(self):
        """
        Reads data from a json file
        :return: data in json format
        """
        try:
            self.json_data = json.load(open(self.input_json_file, 'r'))
            logging.debug('Read data %s', self.json_data)
            # pprint(self._data)
            return self.get_data()
        except FileNotFoundError:
            logging.warning("Could not open data file " + self.input_json_file)

    def read_from_csv_file(self):
        """
        Reads data from a csv file
        :return: data in json format if self.json_format has been defined or plain if not
        """
        try:
            with open(self.input_csv_file, 'r', newline='') as csvfile:
                try:
                    for row in csv.reader(csvfile, delimiter=' ', skipinitialspace=True, quoting=csv.QUOTE_NONE):
                        row = [col.strip() for col in row]
                        row = list(filter(None, row))  # remove empty fields if present
                        self._raw_data.append(row)
                except Exception as e:
                    raise e
        except Exception as e:
            logging.error("Could not read data file " + self.input_csv_file + str(e))

        if self.json_format:
            for row in self._raw_data:
                # logging.debug('row - %s', row)
                # logging.debug('json template - %s', self.json_format)
                temp = zip(self.json_format, row)
                temp3 = {}
                for tuple in temp:
                    temp2 = dict(zip(tuple[::2], tuple[1::2]))
                    #logging.debug('temp2 - %s', temp2)
                    temp3.update(temp2)
                print (json.dumps(temp3))
                self.json_data.append(temp3)


                #json_item = json.JSONEncoder().encode(temp_json)
                #logging.debug('encoded data - %s', json_item)
        return self.json_data

    def get_data(self):
        """ Returns data structure"""
        return self.json_data
