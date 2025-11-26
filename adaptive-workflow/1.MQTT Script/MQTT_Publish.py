
import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Broker details
broker = "3.6.210.66"
port = 1883
username = "mqtt_user"
password = "Apriso2020"
topic = "mes/linedata"

client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port, 60)

machine_status = ["Running", "Down", "Maintenance"]
quality_trend = ["Pass", "Fail"]
operator_availability = ["Available", "Unavailable"]

while True:
    payload = {
        "MachineStatus": random.choice(machine_status),
        "QualityTrend": random.choice(quality_trend),
        "ProductionTarget": random.randint(80, 120),
        "ProductionActual": random.randint(50, 120),
        "OperatorAvailability": random.choice(operator_availability),
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    client.publish(topic, json.dumps(payload))
    print("Published:", payload)
    time.sleep(5)