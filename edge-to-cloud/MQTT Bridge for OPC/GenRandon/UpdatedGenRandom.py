
from opcua import Client, ua
import random
import time

client = Client("opc.tcp://localhost:55000")
print("Connecting to OPC UA Server at opc.tcp://localhost:55000...")
client.connect()
print("Connected!")

try:
    nodes = {
        "MyStoredVariable": client.get_node("ns=1;s=Objects/MyFolder/MyStoredVariable"),
        "MySynchronousVariable": client.get_node("ns=1;s=Objects/MyFolder/MySynchronousVariable"),
        "MyAsynchronousVariable": client.get_node("ns=1;s=Objects/MyFolder/MyAsynchronousVariable")
    }

    while True:
        for name, node in nodes.items():
            value = random.randint(0, 100)
            print(f"Writing {name}: {value}")
            variant = ua.Variant(value, ua.VariantType.UInt32)
            node.set_value(variant)
        time.sleep(0.5)

except Exception as e:
    print("Error:", e)

finally:
    client.disconnect()
    print("Disconnected from OPC UA Server.")
