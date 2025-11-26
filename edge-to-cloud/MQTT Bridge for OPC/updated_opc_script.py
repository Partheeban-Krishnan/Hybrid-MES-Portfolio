import json
import time
from opcua import Client, ua
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
# OPC UA Server details
OPC_SERVER_URL = "opc.tcp://localhost:55000"
# Replace this with the actual NodeId of your MyStoredVariable
# This format uses a string identifier, which is likely correct.
OPC_VARIABLE_NODEID = "ns=2;s=MyStoredVariable"

# MQTT Broker details
# Replace with your EC2 instance's public IP or domain name
MQTT_BROKER_HOST = "52.66.233.45"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "opc_data/my_variable"
MQTT_USERNAME = "mqtt_user"  # Replace with your username
MQTT_PASSWORD = "Apriso2020"  # Replace with your password

# --- GLOBAL MQTT CLIENT ---
# Fix for the DeprecationWarning
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected successfully to MQTT Broker on EC2!")
    elif rc == 5:
        print("Connection failed: Bad user name or password.")
    else:
        print(f"Failed to connect, return code {rc}\n")

mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)


# --- OPC UA SUBSCRIPTION HANDLER ---
# This class handles the data changes from the OPC UA subscription
class SubHandler:
    """
    Subscription Handler for opcua library.
    It receives data changes and publishes them via MQTT.
    """
    def datachange_notification(self, node, val, data):
        print(f"New data from OPC UA: {val.Value.Value}")

        # Prepare the data in a JSON format
        payload = {
            "node_id": str(node.nodeid),
            "value": val.Value.Value,
            "timestamp": str(val.SourceTimestamp)
        }

        # Publish the data to the MQTT broker
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Published to MQTT topic '{MQTT_TOPIC}'")

# --- MAIN SYNCHRONOUS FUNCTION ---
def main():
    # Connect to the MQTT broker first
    try:
        print(f"Connecting to MQTT Broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
        mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Could not connect to MQTT Broker: {e}")
        return

    # Connect to the OPC UA server
    try:
        opc_client = Client(url=OPC_SERVER_URL)
        print(f"Connecting to OPC UA Server at {OPC_SERVER_URL}...")
        opc_client.connect()

        # Get the node for your variable
        opc_variable = opc_client.get_node(OPC_VARIABLE_NODEID)

        # Create a subscription to monitor the variable
        handler = SubHandler()
        subscription = opc_client.create_subscription(500, handler)
        subscription.subscribe_data_change(opc_variable)

        print("Subscription created. Monitoring for data changes...")
        print("To test, manually change the value of 'MyStoredVariable' from the OPC UA client.")

        # Keep the script running to listen for changes
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Could not connect to OPC UA Server: {e}")
    finally:
        if 'opc_client' in locals() and opc_client.is_connected:
            opc_client.disconnect()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Disconnected from all services.")

# --- RUN THE SCRIPT ---
if __name__ == "__main__":
    main()
