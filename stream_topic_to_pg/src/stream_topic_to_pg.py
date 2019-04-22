import os
import json
import sys
import pendulum

from model import ResponseTime
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")
PG_URI = os.environ.get("PG_URI")

try:
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=json.loads,
    )
except NoBrokersAvailable:
    sys.exit("No broker available")

engine = create_engine(PG_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

for ind, message in enumerate(consumer):
    msg = message.value
    route = msg["Route"]
    time = msg["ResponseTime"] / 1e9  # in seconds
    request_time = pendulum.parse(msg["RequestTimeStamp"])
    row = ResponseTime(route=route, time=time, request_time=request_time)
    session.add(row)
    session.commit()

