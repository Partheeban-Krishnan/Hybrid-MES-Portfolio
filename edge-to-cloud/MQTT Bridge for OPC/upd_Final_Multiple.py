
import json
import time
from opcua import Client
from opcua.ua import NodeId
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
OPC_SERVER_URL = "opc.tcp://localhost:55000"
OPC_VARIABLE_NODEIDS = {
    "MyStoredVariable": "ns=1;s=Objects/MyFolder/MyStoredVariable",
    "MySynchronousVariable": "ns=1;s=Objects/MyFolder/MySynchronousVariable",
    "MyAsynchronousVariable": "ns=1;s=Objects/MyFolder/MyAsynchronousVariable"
}

MQTT_BROKER_HOST = "13.202.139.5"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "opc_data/all_variables"
MQTT_USERNAME = "mqtt_user"
MQTT_PASSWORD = "Apriso2020"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Dictionary to store latest values
latest_values = {}

class SubHandler:
    def datachange_notification(self, node, val, data):
        for name, nodeid_str in OPC_VARIABLE_NODEIDS.items():
            expected_nodeid = NodeId.from_string(nodeid_str)
            if node.nodeid == expected_nodeid:
                latest_values[name] = val
                break

        payload = {
            "timestamp": str(data.monitored_item.Value.SourceTimestamp),
            "variables": latest_values
        }

        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Published combined data: {payload}")

def main():
    try:
        print(f"Connecting to MQTT Broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
        mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        mqtt_client.loop_start()

        opc_client = Client(OPC_SERVER_URL)
        print(f"Connecting to OPC UA Server at {OPC_SERVER_URL}...")
        opc_client.connect()

        handler = SubHandler()
        subscription = opc_client.create_subscription(500, handler)

        for name, nodeid_str in OPC_VARIABLE_NODEIDS.items():
            node = opc_client.get_node(nodeid_str)
            subscription.subscribe_data_change(node)
            latest_values[name] = None

        print("Monitoring multiple OPC UA variables...")
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'opc_client' in locals() and opc_client.is_connected:
            opc_client.disconnect()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Disconnected from all services.")

if __name__ == "__main__":
    main()
