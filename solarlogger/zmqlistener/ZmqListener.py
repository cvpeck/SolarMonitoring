# -*- coding: utf-8 -*-
#
""" Zmq Listener """
import logging
import zmq
import queue
import threading


class ZmqListener:
    """
    Listens to ZMQ socket
    """

    def __init__(self):
        self.port = ''
        self.zmq_publisher_address = '127.0.0.1'
        self.topic = ''  # An empty string will subscribe to all topics
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self.is_socket_open = False
        self.data = []
        self.log_level = logging.DEBUG
        logging.basicConfig(level=self.log_level)
        self.logger = logging.getLogger(__name__)
        self.data_queue = queue.Queue()
        self.is_data_queue_full = False
        self.producer_thread = None
        self.is_thread_started = False

    def set_log_level(self, level):
        self.logger.setLevel(level)


    def open_zmq(self):
        """
        opens zmq socket for listening
        :return:
        """
        if not self.is_socket_open:
            if self.port == '':
                self.logger.error('ZMQ port to listen to has not been defined')
            else:
                try:
                    self._socket.connect('tcp://%s:%s' % (self.zmq_publisher_address, self.port))
                    self._socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
                    self.is_socket_open = True
                except zmq.error.ZMQError as e:
                    self.logger.error("Could connect to  " + self.zmq_publisher_address + self.port)
                    raise e

    def start_thread(self):
        self.producer_thread = ProducerThread(name='producer_of_data_consumer_of_zmq_messages', queue=self.data_queue, instance=self)
        self.producer_thread.start()


    def stop_thread(self):
        self.logger.debug("Thread shutdown")
        self.producer_thread.stop()

    def receive_zmq_messages(self):
        """
        Displays zmq messages from subscription in a continually running loop
        :return:
        """


class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, queue=None, instance=None):
        super(ProducerThread, self).__init__()
        self.target = target
        self.name = name
        self.queue = queue
        self._instance = instance
        return

    def run(self):
        self._instance.is_thread_started = True
        self._instance.logger.info('ZMQ Listener listening to tcp://%s:%s' % (self._instance.zmq_publisher_address, self._instance.port))
        while True:
            string = self._instance._socket.recv().decode('utf-8')
            # pprint (string.split())
            received_topic, received_data = string.split('{')
            self._instance.logger.debug('Received ZMQ topic: %s message: %s' % (received_topic, received_data))
            if not self._instance.data_queue.full():
                self._instance.is_data_queue_full = False
                self._instance.data_queue.put(received_data)
            else:
                self._instance.logger.error('Data queue full')
                self._instance.is_data_queue_full = True

        return
