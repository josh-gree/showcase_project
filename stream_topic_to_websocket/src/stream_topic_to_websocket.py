import sys
import os
import json
import datetime
import asyncio
import websockets

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC = os.environ.get("TOPIC")

try:
    consumer = KafkaConsumer(
        TOPIC, bootstrap_servers=KAFKA_BROKER_URL, value_deserializer=json.loads
    )
except NoBrokersAvailable:
    sys.exit("No broker available")


async def consume_to_ws(websocket, path):
    while True:
        for message in consumer:
            await websocket.send(json.dumps(message.value))


start_server = websockets.serve(consume_to_ws, "0.0.0.0", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
