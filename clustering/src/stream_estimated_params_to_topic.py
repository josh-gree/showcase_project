import os
import sys
import json
import time
import psycopg2

from kafka import KafkaProducer
from utils import get_data, get_params

pg_uri = "postgres://pg:pg@pg:5432/pg"

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
PARAMS_TOPIC = os.environ.get("PARAMS_TOPIC")
BOOTSTRAP_SERVERS = os.environ.get("BOOTSTRAP_SERVERS")

try:
    conn = psycopg2.connect(pg_uri)
except Exception as e:
    sys.exit("No pg available")

try:
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS.split(","),
        value_serializer=lambda m: json.dumps(m).encode("ascii"),
    )
except Exception as e:
    sys.exit("No broker available")


while True:

    data = get_data(conn)
    try:
        params = get_params(data)
        producer.send(PARAMS_TOPIC, params)
    except Exception as e:
        params = {}
        producer.send(PARAMS_TOPIC, params)

    print(params)
    time.sleep(2)
