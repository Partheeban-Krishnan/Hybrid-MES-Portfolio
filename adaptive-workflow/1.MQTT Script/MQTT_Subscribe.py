import paho.mqtt.client as mqtt
import json
import pyodbc

broker = "3.6.210.66"
port = 1883
username = "mqtt_user"
password = "Apriso2020"
topic = "mes/linedata"

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com;'
    'DATABASE=TestDB;UID=admin;PWD=Apriso2020;Encrypt=yes;TrustServerCertificate=yes;'
)
cursor = conn.cursor()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(topic)
    print("Subscribed to:", topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("Received:", data)
        cursor.execute("""
            INSERT INTO MESData (MachineStatus, QualityTrend, ProductionTarget, ProductionActual, OperatorAvailability, Timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["MachineStatus"],
            data["QualityTrend"],
            data["ProductionTarget"],
            data["ProductionActual"],
            data["OperatorAvailability"],
            data["Timestamp"]
        ))
        conn.commit()
        print("Inserted into RDS:", data)
    except Exception as e:
        print("Error:", e)

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_forever()