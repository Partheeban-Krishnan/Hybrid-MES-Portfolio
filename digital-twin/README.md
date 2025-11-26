# Digital Twin in Action: Real-Time Monitoring + ML-Driven Insights

## Description
This POC demonstrates how Digital Twin technology can be integrated with MES data to provide immersive 3D visualization, real-time monitoring, and predictive insights using machine learning. It goes beyond static dashboards by enabling contextual awareness and automated workflows for anomaly handling.

## Architecture Diagram
<img width="940" height="675" alt="image" src="https://github.com/user-attachments/assets/a6f59326-9e3b-4633-b8c4-c4fcac296fa4" />

## Digital Twin Dashboard
<img width="940" height="429" alt="image" src="https://github.com/user-attachments/assets/7bd12576-1770-4a97-a1ed-72fa504d4d21" />

## Production Health Dashboard
<img width="940" height="384" alt="image" src="https://github.com/user-attachments/assets/d60e179e-bfc3-4030-b202-977cf4292105" />


## What was implemented
**System Architecture**
- Data Flow: Edge → MQTT / REST API / OPC UA → AWS RDS (SQL Server)
- Visualization: Grafana dashboards with a tabbed layout for Digital Twin & Production Health
- 3D Model & Real-Time Monitoring: AWS IoT TwinMaker for immersive scenes and live property updates (Flask-based video streaming as a Kinesis-free alternative)
- Graph Context: Neo4j for machine relationships, integrated via PyVis + Flask on EC2
- AWS Services: EC2, RDS, IoT TwinMaker, Lambda, Step Functions, SNS, SageMaker AI, S3 for storage
  
**ML Intelligence**
- Isolation Forest detects anomalies from MES data
- Automated via Windows Task Scheduler → Inserts anomaly KPIs into RDS
  
**Workflow Automation**
- AWS Step Functions orchestrate maintenance workflows
- SNS sends alerts and Human-in-the-Loop approvals
- Maintenance orders auto-created in RDS upon approval

## Why This Matters
**This is not just a dashboard—it’s a closed-loop Digital Twin:**
- Immersive Monitoring: Live machine data synced with 3D models
- Contextual Awareness: Graph relationships highlight anomalies (red node) and impact zones
- Predictive Insights: ML-driven health status integrated directly into visualization
- Actionable Automation: Alerts trigger workflows and resource allocation instantly


## Business Impact
- ⚡ Agility: Operators act on anomalies in seconds
- 🔍 Visibility: Unified view of machine health + process context
- 📈 Scalability: Cloud-native design supports multi-plant deployments
- 🔒 Compliance: Human-in-the-Loop approvals for critical events

## Code Snipet

## Code Highlight: AWS IoT TwinMaker Update
```python
client = boto3.client("iottwinmaker", region_name="ap-south-1")

def update_twinmaker(entity_id, machine_id, prod, energy, env):
    update_payload = {
        "componentUpdates": {
            "MachineDataSource": {
                "propertyUpdates": {
                    "MachineID": {"value": {"stringValue": machine_id}},
                    "Status": {"value": {"stringValue": prod['Status']}},
                    "MachineTemp": {"value": {"doubleValue": float(prod['Temperature'])}}
                }
            }
        }
    }
    response = client.update_entity(
        workspaceId="DigitalTwin",
        entityId=entity_id,
        componentUpdates=update_payload["componentUpdates"]
    )
    print(f"Update successful for {machine_id}: {response['updateDateTime']}")

**Full script available in digital-twin folder.**
```
