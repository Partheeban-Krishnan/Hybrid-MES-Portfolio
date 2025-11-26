
import paho.mqtt.client as mqtt
import json
import pyodbc

# MQTT Broker details
broker = "43.205.141.247"
port = 1883
username = "mqtt_user"
password = "Apriso2020"
topic = "mes/production/data"

# SQL Server RDS connection with SSL fix
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com;'
    'DATABASE=TestDB;'
    'UID=admin;'
    'PWD=Apriso2020;'
    'Encrypt=yes;TrustServerCertificate=yes;'
)
cursor = conn.cursor()

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        datatype = data.get("DataType")
        payload = json.dumps(data.get("Payload"))

        cursor.execute(
            "INSERT INTO MES_Data (DataType, Payload) VALUES (?, ?)",
            datatype, payload
        )
        conn.commit()
        print("Inserted into RDS:", data)
    except Exception as e:
        print("Error:", e)

# MQTT client setup
client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port, 60)
client.subscribe(topic)
client.on_message = on_message
client.loop_forever()

