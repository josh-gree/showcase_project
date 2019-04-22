import sys
import os
import json
import datetime
import asyncio
import websockets

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")

try:
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=json.loads,
    )
except NoBrokersAvailable:
    sys.exit("No broker available")


async def consume_to_ws(websocket, path):
    while True:
        for message in consumer:
            msg_dict = {
                "route": message.value["Route"],
                "response_time_in_s": message.value["ResponseTime"] / 1e-9,
            }
            await websocket.send(json.dumps(msg_dict))


start_server = websockets.serve(consume_to_ws, "0.0.0.0", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
