
import json
import time
from opcua import Client
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
OPC_SERVER_URL = "opc.tcp://localhost:55000"
OPC_VARIABLE_NODEID = "ns=1;s=Objects/MyFolder/MyStoredVariable"

MQTT_BROKER_HOST = "3.110.149.244"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "opc_data/my_variable"
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

class SubHandler:
    def datachange_notification(self, node, val, data):
        print(f"New OPC UA Value: {val}")
        payload = {
            "node_id": str(node.nodeid),
            "value": val,
            "timestamp": str(data.monitored_item.Value.SourceTimestamp)
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Published to MQTT topic '{MQTT_TOPIC}'")

def main():
    try:
        print(f"Connecting to MQTT Broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
        mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        mqtt_client.loop_start()

        opc_client = Client(OPC_SERVER_URL)
        print(f"Connecting to OPC UA Server at {OPC_SERVER_URL}...")
        opc_client.connect()

        opc_variable = opc_client.get_node(OPC_VARIABLE_NODEID)
        handler = SubHandler()
        subscription = opc_client.create_subscription(500, handler)
        subscription.subscribe_data_change(opc_variable)

        print("Monitoring OPC UA variable for changes...")
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
