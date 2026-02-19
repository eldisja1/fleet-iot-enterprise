import time
import json
import uuid
import random
import math
from datetime import datetime
import paho.mqtt.client as mqtt
import os

import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_BASE_TOPIC = os.getenv("MQTT_TOPIC", "fleet")



PUBLISH_INTERVAL = 5
NUMBER_OF_DEVICES = 5

class DeviceSimulator:
    def __init__(self, device_id):
        self.device_id = device_id
        self.lat = -6.200000  # Jakarta
        self.lon = 106.816666
        self.speed = random.uniform(20, 80)  # km/h
        self.fuel_level = 100.0
        self.online = True

    def simulate_movement(self):
        # Simple movement calculation
        delta = self.speed / 111000  # approx deg conversion
        angle = random.uniform(0, 2 * math.pi)

        self.lat += delta * math.cos(angle)
        self.lon += delta * math.sin(angle)

    def simulate_fuel(self):
        consumption = self.speed * 0.0005
        self.fuel_level -= consumption
        if self.fuel_level < 0:
            self.fuel_level = 0

    def simulate_online_status(self):
        # 5% chance to go offline
        if random.random() < 0.05:
            self.online = False
        # 10% chance to come back online
        elif random.random() < 0.10:
            self.online = True

    def generate_payload(self):
        return {
            "device_id": self.device_id,
            "timestamp": datetime.utcnow().isoformat(),
            "latitude": self.lat,
            "longitude": self.lon,
            "speed": round(self.speed, 2),
            "fuel_level": round(self.fuel_level, 2),
            "status": "online" if self.online else "offline"
        }


def main():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    devices = [
        DeviceSimulator(str(uuid.uuid4()))
        for _ in range(NUMBER_OF_DEVICES)
    ]

    while True:
        for device in devices:
            device.simulate_online_status()

            if device.online:
                device.simulate_movement()
                device.simulate_fuel()
                payload = device.generate_payload()
                topic = f"{MQTT_BASE_TOPIC}/{device.device_id}/telemetry"
                client.publish(topic, json.dumps(payload))
                print(f"Published: {payload}")
            else:
                print(f"Device {device.device_id} is offline")
        time.sleep(PUBLISH_INTERVAL)


if __name__ == "__main__":
    main()
