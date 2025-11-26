
from flask import Flask, request
from pyvis.network import Network
from neo4j import GraphDatabase
import os

# Flask app initialization
app = Flask(__name__)

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Apriso2020"
DATABASE_NAME = "mesgraph"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Colors and sizes for node types
colors = {
    "Asset": "#1f77b4",            # Blue
    "ProductionRecord": "#ff7f0e", # Orange
    "Anomaly": "#d62728",          # Red
    "MaintenanceEvent": "#2ca02c", # Green
    "EnergyMetric": "#9467bd",     # Purple
    "EnvironmentalMetric": "#8c564b" # Brown
}

sizes = {
    "Asset": 40,
    "ProductionRecord": 25,
    "Anomaly": 15,
    "MaintenanceEvent": 15,
    "EnergyMetric": 15,
    "EnvironmentalMetric": 15
}

@app.route("/graph")
def graph():
    machine_id = request.args.get("machineID")
    if not machine_id:
        return "<h3>Error: Please provide machineID in URL, e.g., /graph?machineID=MCH100</h3>"

    # Create PyVis network
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")
    net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=150, spring_strength=0.08)
    net.toggle_physics(True)
    net.show_buttons(filter_=['physics', 'nodes'])

    # Cypher query for selected machine
    query = """
    MATCH (a:Asset {MachineID:$machineID})-[:HAS_PRODUCTION]->(p:ProductionRecord)
    OPTIONAL MATCH (p)-[:HAS_ANOMALY]->(an:Anomaly)
    OPTIONAL MATCH (p)-[:HAS_MAINTENANCE]->(m:MaintenanceEvent)
    OPTIONAL MATCH (p)-[:HAS_ENERGY]->(e:EnergyMetric)
    OPTIONAL MATCH (p)-[:HAS_ENVIRONMENT]->(env:EnvironmentalMetric)
    RETURN a.AssetName AS asset, p.RecordID AS production,
           collect(DISTINCT an.AnomalyFlag) AS anomalies,
           collect(DISTINCT m.MaintenanceType) AS maintenances,
           collect(DISTINCT e.EnergyID) AS energies,
           collect(DISTINCT env.EnvID) AS environments
    """

    with driver.session(database=DATABASE_NAME) as session:
        result = session.run(query, machineID=machine_id)
        records = list(result)

        if not records:
            return f"<h3>No data found for MachineID: {machine_id}</h3>"

        for record in records:
            asset = str(record["asset"])
            production = str(record["production"])

            # Add Asset node
            net.add_node(asset, label=asset, color=colors["Asset"], size=sizes["Asset"],
                         title=f"Type: Asset\nID: {asset}",
                         url=f"http://grafana-dashboard/assets/{asset}")

            # Add ProductionRecord node
            net.add_node(production, label=production, color=colors["ProductionRecord"], size=sizes["ProductionRecord"],
                         title=f"Type: ProductionRecord\nID: {production}",
                         url=f"http://grafana-dashboard/production/{production}")

            net.add_edge(asset, production)

            # Add related nodes
            for anomaly in record["anomalies"]:
                if anomaly:
                    anomaly_id = str(anomaly)
                    net.add_node(anomaly_id, label=anomaly_id, color=colors["Anomaly"], size=sizes["Anomaly"],
                                 title=f"Type: Anomaly\nID: {anomaly_id}")
                    net.add_edge(production, anomaly_id)

            for maintenance in record["maintenances"]:
                if maintenance:
                    maintenance_id = str(maintenance)
                    net.add_node(maintenance_id, label=maintenance_id, color=colors["MaintenanceEvent"], size=sizes["MaintenanceEvent"],
                                 title=f"Type: MaintenanceEvent\nID: {maintenance_id}")
                    net.add_edge(production, maintenance_id)

            for energy in record["energies"]:
                if energy:
                    energy_id = str(energy)
                    net.add_node(energy_id, label=energy_id, color=colors["EnergyMetric"], size=sizes["EnergyMetric"],
                                 title=f"Type: EnergyMetric\nID: {energy_id}")
                    net.add_edge(production, energy_id)

            for environment in record["environments"]:
                if environment:
                    environment_id = str(environment)
                    net.add_node(environment_id, label=environment_id, color=colors["EnvironmentalMetric"], size=sizes["EnvironmentalMetric"],
                                 title=f"Type: EnvironmentalMetric\nID: {environment_id}")
                    net.add_edge(production, environment_id)

    # Save HTML in current directory
    html_file = os.path.join(os.getcwd(), f"{machine_id}_graph.html")
    net.write_html(html_file)

    # Return HTML content
    return open(html_file, "r", encoding="utf-8").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
