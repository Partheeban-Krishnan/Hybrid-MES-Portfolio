
from opcua import Client, ua
import random
import time

# Connect to the OPC UA server
client = Client("opc.tcp://localhost:55000")
print("Connecting to OPC UA Server at opc.tcp://localhost:55000...")
client.connect()
print("Connected!")

try:
    # Use the correct NodeId from your server
    node = client.get_node("ns=1;s=Objects/MyFolder/MyStoredVariable")

    while True:
        value = random.randint(0, 100)
        print("Writing random value:", value)

        # Ensure the value is wrapped with the correct Variant type
        variant = ua.Variant(value, ua.VariantType.UInt32)
        node.set_value(variant)

        time.sleep(2)

except Exception as e:
    print("Error:", e)

finally:
    client.disconnect()
    print("Disconnected from OPC UA Server.")
