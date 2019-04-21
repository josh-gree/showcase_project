import os
import json
import sys

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
    time = msg["ResponseTime"] / 1e-9  # in seconds
    row = ResponseTime(route=route, time=time)
    session.add(row)
    if ind % 100 == 0:
        session.commit()
        print(session.query(ResponseTime).all())
