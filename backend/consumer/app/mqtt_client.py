import json
import logging
import paho.mqtt.client as mqtt
from sqlalchemy.exc import SQLAlchemyError

from .config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from .database import SessionLocal
from .models import Telemetry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        logging.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    logging.info(f"Received message on topic {msg.topic}")

    try:
        payload = json.loads(msg.payload.decode())
        
        session = SessionLocal()

        telemetry = Telemetry(
            device_id=payload["device_id"],
            latitude=payload.get("latitude"),
            longitude=payload.get("longitude"),
            speed=payload.get("speed"),
        )

        session.add(telemetry)
        session.commit()
        session.close()

        logging.info("Telemetry inserted successfully")

    except json.JSONDecodeError:
        logging.error("Invalid JSON format")

    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
