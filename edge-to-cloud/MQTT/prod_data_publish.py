
import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Broker details
broker = "13.202.139.5"
port = 1883
username = "mqtt_user"
password = "Apriso2020"
topic = "mes/production/data"

client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port, 60)

def generate_data():
    return {
        "DataType": random.choice(["Production", "Quality"]),
        "Payload": {
            "MachineID": f"M{random.randint(1,5)}",
            "Value": round(random.uniform(10.0, 99.9), 2),
            "Unit": "pcs"
        }
    }

while True:
    data = generate_data()
    client.publish(topic, json.dumps(data))
    print("Published:", data)
    time.sleep(5)

