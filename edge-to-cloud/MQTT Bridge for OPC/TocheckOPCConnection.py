
from opcua import Client

client = Client("opc.tcp://localhost:55000")
client.connect()
node = client.get_node("ns=1;s=Objects/MyFolder/MyStoredVariable")  # Replace with your actual node ID
datatype = node.get_data_type_as_variant_type()
print("Expected data type:", datatype)
client.disconnect()
