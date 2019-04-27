import os
import json
import sys
import logging
import asyncio

import threading

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.platform.asyncio

from tornado.web import Application

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


class KafkaWebSocket(tornado.websocket.WebSocketHandler):
    open_sockets = set()

    def check_origin(self, origin):
        return True

    @classmethod
    def write_to_all(cls, message):
        removable = set()
        for ws in cls.open_sockets:
            if not ws.ws_connection or not ws.ws_connection.stream.socket:
                removable.add(ws)
            else:
                ws.write_message(message)
        for ws in removable:
            cls.open_sockets.remove(ws)

    def open(self):
        type(self).open_sockets.add(self)


class Consumer(threading.Thread):
    daemon = True

    def __init__(self, kafka_consumer):
        self._consumer = kafka_consumer
        super(Consumer, self).__init__()

    def run(self):
        for message in self._consumer:
            data = json.dumps(message.value)
            KafkaWebSocket.write_to_all(data)


if __name__ == "__main__":

    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
    TOPIC = os.environ.get("TOPIC")

    port = 5678
    address = "0.0.0.0"

    asyncio.set_event_loop_policy(tornado.platform.asyncio.AnyThreadEventLoopPolicy())

    try:
        Kconsumer = KafkaConsumer(
            TOPIC, bootstrap_servers=KAFKA_BROKER_URL, value_deserializer=json.loads
        )
    except NoBrokersAvailable:
        sys.exit("No broker available")

    kafka_consumer = Consumer(Kconsumer)
    kafka_consumer.start()

    routes = [(r"/", KafkaWebSocket)]
    application = Application(routes)
    application.listen(port=port, address=address)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except (KeyboardInterrupt, SystemExit):
        pass
