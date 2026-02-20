import json
import logging
import uuid

import paho.mqtt.client as mqtt
from sqlalchemy.exc import SQLAlchemyError

from .config import MQTT_BROKER, MQTT_PORT, MQTT_SUBSCRIBE_TOPIC
from .database import SessionLocal
from .models import Telemetry, Device


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================
# MQTT CALLBACKS
# ==============================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker")

        client.subscribe(MQTT_SUBSCRIBE_TOPIC)
        logging.info(f"Subscribed to topic: {MQTT_SUBSCRIBE_TOPIC}")

    else:
        logging.error(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    logging.info(f"Received message on topic {msg.topic}")

    session = SessionLocal()

    try:
        payload = json.loads(msg.payload.decode())

        # ==============================
        # Validate required field
        # ==============================
        if "device_id" not in payload:
            raise KeyError("device_id")

        device_uuid = uuid.UUID(payload["device_id"])

        # ==============================
        # Auto Device Provisioning
        # ==============================
        device = session.query(Device).filter(Device.id == device_uuid).first()

        if not device:
            logging.info(f"New device detected: {device_uuid}")

            device = Device(
                id=device_uuid,
                device_code=str(device_uuid),
                name=f"Device-{str(device_uuid)[:8]}",
                status="online"
            )

            session.add(device)
            session.commit()
            logging.info("Device registered successfully")

        # ==============================
        # Insert Telemetry
        # ==============================
        telemetry = Telemetry(
            device_id=device_uuid,
            latitude=payload.get("latitude"),
            longitude=payload.get("longitude"),
            speed=payload.get("speed"),
            fuel_level=payload.get("fuel_level"),
            status=payload.get("status"),
        )

        session.add(telemetry)
        session.commit()

        logging.info("Telemetry inserted successfully")

    except json.JSONDecodeError:
        session.rollback()
        logging.error("Invalid JSON format")

    except ValueError:
        session.rollback()
        logging.error("Invalid UUID format for device_id")

    except KeyError as e:
        session.rollback()
        logging.error(f"Missing required field: {e}")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Database error: {e}")

    except Exception as e:
        session.rollback()
        logging.error(f"Unexpected error: {e}")

    finally:
        session.close()


# ==============================
# START MQTT
# ==============================

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    logging.info("Starting MQTT loop...")
    client.loop_forever()