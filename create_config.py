import configparser

config = configparser.ConfigParser()
config['SERIALPORT'] = {'Device': '/dev.xx1',
    'Speed':    '9600',
    'DataBits': '8',
    'Parity': 'N',
    'Stop': '1'};

config['ZMQ'] = {'Port': '6745'};

with open('solar.ini', 'w') as configfile:
    config.write(configfile)
