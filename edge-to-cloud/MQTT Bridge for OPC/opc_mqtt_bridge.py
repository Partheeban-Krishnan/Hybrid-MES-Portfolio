import asyncio
import json
from asyncua import Client, ua
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
# OPC UA Server details
OPC_SERVER_URL = "opc.tcp://localhost:55000"
# Replace this with the actual NodeId of your MyStoredVariable
OPC_VARIABLE_NODEID = "ns=2;i=1011"

# MQTT Broker details
# Replace with your EC2 instance's public IP or domain name
MQTT_BROKER_HOST = "52.66.233.45"
MQTT_BROKER_PORT = 1883  # Use 1883 for unsecured MQTT
# The topic to publish the OPC UA data to
MQTT_TOPIC = "opc_data/my_variable"
# Path to your MQTT certificates
# These are not needed for unsecured connections on port 1883
# CA_CERTS_PATH = "path/to/your/ca.crt"
# CLIENT_CERT_PATH = "path/to/your/client.crt"
# CLIENT_KEY_PATH = "path/to/your/client.key"

# --- GLOBAL MQTT CLIENT ---
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# --- MQTT CALLBACKS (Optional but good practice) ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT Broker on EC2!")
    else:
        print(f"Failed to connect, return code {rc}\n")

mqtt_client.on_connect = on_connect

# Configure TLS for secure connection
# These lines have been removed because you are using the unsecured port 1883
# mqtt_client.tls_set(
#     ca_certs=CA_CERTS_PATH,
#     certfile=CLIENT_CERT_PATH,
#     keyfile=CLIENT_KEY_PATH
# )

# --- OPC UA SUBSCRIPTION HANDLER ---
# This class handles the data changes from the OPC UA subscription
class SubHandler:
    """
    Subscription Handler.
    This class is the OPC UA-to-MQTT bridge.
    It receives data changes and publishes them via MQTT.
    """
    def datachange_notification(self, node, val, data):
        print(f"New data from OPC UA: {val}")

        # Prepare the data in a JSON format
        payload = {
            "node_id": str(node),
            "value": val,
            "timestamp": str(data.monitored_item.Value.SourceTimestamp)
        }

        # Publish the data to the MQTT broker
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Published to MQTT topic '{MQTT_TOPIC}'")

# --- MAIN ASYNCHRONOUS FUNCTION ---
async def main():
    # Connect to the MQTT broker first
    try:
        mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Could not connect to MQTT Broker: {e}")
        return

    # Connect to the OPC UA server
    try:
        async with Client(url=OPC_SERVER_URL) as opc_client:
            print(f"Connected to OPC UA Server at {OPC_SERVER_URL}")

            # Get the node for your variable
            opc_variable = opc_client.get_node(OPC_VARIABLE_NODEID)

            # Create a subscription to monitor the variable
            handler = SubHandler()
            subscription = await opc_client.create_subscription(500, handler)
            await subscription.subscribe_data_change(opc_variable)

            print("Subscription created. Monitoring for data changes...")
            print("To test, manually change the value of 'MyStoredVariable' from the OPC UA client.")

            # Keep the script running to listen for changes
            await asyncio.Future()

    except Exception as e:
        print(f"Could not connect to OPC UA Server: {e}")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Disconnected from all services.")

# --- RUN THE SCRIPT ---
if __name__ == "__main__":
    asyncio.run(main())
