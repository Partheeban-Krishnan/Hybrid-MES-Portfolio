
from pyvis.network import Network
from neo4j import GraphDatabase

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Apriso2020"
DATABASE_NAME = "mesgraph"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Create PyVis network with physics enabled
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=150, spring_strength=0.08)
net.toggle_physics(True)

# Enable filtering buttons
net.show_buttons(filter_=['physics', 'nodes'])

# Color coding by type
colors = {
    "Asset": "#1f77b4",            # Blue
    "ProductionRecord": "#ff7f0e", # Orange
    "Anomaly": "#d62728",          # Red
    "MaintenanceEvent": "#2ca02c", # Green
    "EnergyMetric": "#9467bd",     # Purple
    "EnvironmentalMetric": "#8c564b" # Brown
}

# Node size by type
sizes = {
    "Asset": 40,
    "ProductionRecord": 25,
    "Anomaly": 15,
    "MaintenanceEvent": 15,
    "EnergyMetric": 15,
    "EnvironmentalMetric": 15
}

# Cypher query
query = """
MATCH (a:Asset)-[:HAS_PRODUCTION]->(p:ProductionRecord)
OPTIONAL MATCH (p)-[:HAS_ANOMALY]->(an:Anomaly)
OPTIONAL MATCH (p)-[:HAS_MAINTENANCE]->(m:MaintenanceEvent)
OPTIONAL MATCH (p)-[:HAS_ENERGY]->(e:EnergyMetric)
OPTIONAL MATCH (p)-[:HAS_ENVIRONMENT]->(env:EnvironmentalMetric)
RETURN a.AssetName AS asset,
       p.RecordID AS production,
       collect(DISTINCT an.AnomalyFlag) AS anomalies,
       collect(DISTINCT m.MaintenanceType) AS maintenances,
       collect(DISTINCT e.EnergyID) AS energies,
       collect(DISTINCT env.EnvID) AS environments
LIMIT 10
"""

with driver.session(database=DATABASE_NAME) as session:
    result = session.run(query)
    for record in result:
        asset = str(record["asset"])
        production = str(record["production"])

        # Add Asset node with clickable link
        net.add_node(asset, label=asset, color=colors["Asset"], size=sizes["Asset"],
                     title=f"Type: Asset\nID: {asset}",
                     url=f"http://grafana-dashboard/assets/{asset}")

        # Add ProductionRecord node
        net.add_node(production, label=production, color=colors["ProductionRecord"], size=sizes["ProductionRecord"],
                     title=f"Type: ProductionRecord\nID: {production}",
                     url=f"http://grafana-dashboard/production/{production}")

        # Edge between Asset and ProductionRecord
        net.add_edge(asset, production)

        # Add related nodes and edges
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

# Generate HTML
html_file = "neo4j_graph_interactive.html"
net.write_html(html_file, open_browser=True)
print(f"Interactive graph generated: {html_file}")
