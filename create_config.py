import configparser

config = configparser.ConfigParser()
config['SERIALPORT'] = {
    'Device': 'FT0K3AEM',
    'baud':    '9600',
    'DataBits': '8',
    'Parity': 'N',
    'Stop': '1'};

config['ZMQ'] = {'Port': '6745'};

with open('solar.ini', 'w') as configfile:
    config.write(configfile)
