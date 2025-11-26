# Edge To Cloud Integration

## Description
This POC demonstrates secure, real-time data flow between shop-floor machines and the cloud using a hybrid architecture. It combines MQTT for lightweight messaging and OPC UA for machine connectivity with RESTful APIs for structured, transactional data exchange between MES and enterprise systems.

## Architecture Diagram
## MQTT
<img width="938" height="568" alt="image" src="https://github.com/user-attachments/assets/1f0d84df-b230-404c-a66f-7722ca56a8e6" />

## OPC UA
<img width="944" height="631" alt="image" src="https://github.com/user-attachments/assets/156f601f-f9c7-409d-9e25-38f0f1a71d1d" />

## REST API
<img width="909" height="607" alt="image" src="https://github.com/user-attachments/assets/7b99dc1b-f770-476a-a644-79363167e43a" />

## Technologies Used
- Protocols: MQTT, OPC UA, RESTful Web API
- Messaging Broker: RabbitMQ
- Cloud Services: AWS EC2, AWS RDS (SQL Server)
- Programming: Python (Publisher & Subscriber scripts, REST API calls)
- Security: API Key authentication, HTTPS for REST API
- RESTful Web API for structured enterprise ↔ cloud integration

## Setup Instructions
- Configure RabbitMQ MQTT broker on AWS EC2.
- Deploy Python publisher and subscriber scripts for permanent MQTT connection.
- Set up REST API endpoint on EC2 for transactional data exchange.
- Connect to AWS RDS for data persistence.

## Business Impact
* Real-Time Visibility: Enables instant data exchange between edge devices and cloud systems.
* Structured Integration: REST API ensures secure, firewall-friendly communication with ERP, PLM, and QMS.
* Scalability: Supports multi-plant deployments with modular architecture.
* Foundation for Industry 4.0: Serves as the backbone for advanced MES capabilities like AI-driven analytics and Digital Twin integration.
* Operational Resilience: Maintains local control while providing global insights, even in low-connectivity environments.


## Code Highlight: MQTT Publisher
```python
import paho.mqtt.client as mqtt
import json, time, random

broker = "<your-broker-ip>"
topic = "mes/production/data"
client = mqtt.Client()
client.username_pw_set("mqtt_user", "******")
client.connect(broker, 1883, 60)

def generate_data():
    return {
        "DataType": random.choice(["Production", "Quality"]),
        "Payload": {"MachineID": f"M{random.randint(1,5)}", "Value": round(random.uniform(10.0, 99.9), 2)}
    }

while True:
    data = generate_data()
    client.publish(topic, json.dumps(data))
    print("Published:", data)
    time.sleep(5)
**Full script in edge-to-cloud folder.**
```
## Code Highlight: MQTT Subscriber
```python
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    cursor.execute("INSERT INTO MES_Data (DataType, Payload) VALUES (?, ?)", data["DataType"], json.dumps(data["Payload"]))
    conn.commit()
    print("Inserted into RDS:", data)
**Full script in edge-to-cloud folder.**
```

## Code Highlight: OPC UA to MQTT Bridge
```python
from opcua import Client
import paho.mqtt.client as mqtt
import json

OPC_SERVER_URL = "opc.tcp://localhost:55000"
MQTT_TOPIC = "opc_data/all_variables"

class SubHandler:
    def datachange_notification(self, node, val, data):
        payload = {
            "timestamp": str(data.monitored_item.Value.SourceTimestamp),
            "variables": latest_values
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print("Published combined data:", payload)

# Subscribe to multiple OPC UA variables and publish to MQTT
subscription = opc_client.create_subscription(500, SubHandler())
for nodeid in OPC_VARIABLE_NODEIDS.values():
    node = opc_client.get_node(nodeid)
    subscription.subscribe_data_change(node)
  **Full script in edge-to-cloud folder.**
```

## Code Highlight: REST API Data Posting
```python
import requests, random, time
from datetime import datetime

headers = {"x-api-key": "mysecureapikey123"}  # API Key for authentication
statuses = ["Running", "Idle", "Stopped", "Maintenance"]

while True:
    payload = {
        "machine_id": "M001",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "temperature": round(random.uniform(60.0, 100.0), 2),
        "status": random.choice(statuses)
    }
    response = requests.post("http://<your-api-endpoint>/data", json=payload, headers=headers)
    print(f"Sent: {payload} | Response: {response.status_code}")
    time.sleep(5)
**Full script available in REST-API folder.**
```
