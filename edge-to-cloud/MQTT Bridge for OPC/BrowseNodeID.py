
from opcua import Client
from opcua.ua import NodeClass

OPC_SERVER_URL = "opc.tcp://localhost:55000"

def browse_node(node, level=0):
    indent = "  " * level
    try:
        browse_name = node.get_browse_name()
        node_id = node.nodeid
        node_class = node.get_node_class()
        
        # Print basic info
        print(f"{indent}Node: {browse_name}, NodeId: {node_id}, Class: {node_class}")
        
        # If it's a Variable node, try to read its value
        if node_class == NodeClass.Variable:
            try:
                value = node.get_value()
                print(f"{indent}  Value: {value}")
            except:
                print(f"{indent}  Value: [Cannot read]")
        
        # Recursively browse children
        for child in node.get_children():
            browse_node(child, level + 1)
    except Exception as e:
        print(f"{indent}Error browsing node: {e}")

def main():
    client = Client(OPC_SERVER_URL)
    try:
        print(f"Connecting to OPC UA Server at {OPC_SERVER_URL}...")
        client.connect()
        print("Connected!")

        root = client.get_root_node()
        print("Root Node:", root)

        # Start browsing from Objects folder
        objects = root.get_child(["0:Objects"])
        print("\nBrowsing OPC UA Address Space...\n")
        browse_node(objects)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()
