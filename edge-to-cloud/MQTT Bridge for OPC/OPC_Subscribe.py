
import paho.mqtt.client as mqtt
import json
import pyodbc
from datetime import datetime

# MQTT Broker details
broker = "3.110.149.244"
port = 1883
username = "mqtt_user"
password = "Apriso2020"
topic = "opc_data/all_variables"

# SQL Server RDS connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com;'
    'DATABASE=TestDB;'
    'UID=admin;'
    'PWD=Apriso2020;'
    'Encrypt=yes;TrustServerCertificate=yes;'
)
cursor = conn.cursor()

# MQTT message handler
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        raw_timestamp = data.get("timestamp", "").strip()
        variables = data.get("variables", {})
        MyStoredVariable = variables.get("MyStoredVariable")
        MySynchronousVariable = variables.get("MySynchronousVariable")
        MyAsynchronousVariable = variables.get("MyAsynchronousVariable")

        # Robust timestamp parsing
        try:
            parsed_timestamp = datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError as ve1:
            try:
                parsed_timestamp = datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError as ve2:
                print("Unrecognized timestamp format:", raw_timestamp)
                print("Parsing errors:", ve1, "|", ve2)
                return

        formatted_timestamp = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Insert into SQL Server
        cursor.execute("""
            INSERT INTO opc_data (timestamp, MyStoredVariable, MySynchronousVariable, MyAsynchronousVariable)
            VALUES (?, ?, ?, ?)
        """, (formatted_timestamp, MyStoredVariable, MySynchronousVariable, MyAsynchronousVariable))
        conn.commit()
        print("Inserted into RDS:", data)

    except Exception as e:
        print("Error:", e)

# MQTT client setup (using latest callback API version)
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username, password)
client.connect(broker, port, 60)
client.subscribe(topic)
client.on_message = on_message
client.loop_forever()
