# Adaptive Workflow & Human-in-the-Loop Automation

## Description
This POC demonstrates how MES workflows can be transformed from static processes into adaptive, event-driven workflows that respond dynamically to machine status. It incorporates Human-in-the-Loop (HIL) approvals for critical events, ensuring compliance and security while maintaining agility.

## Architecture Diagram
<img width="940" height="627" alt="image" src="https://github.com/user-attachments/assets/ce8bb93e-01b0-475b-bc3d-70522fba7148" />

## AWS StepFunction
  ## Main Workflow
  <img width="1588" height="679" alt="image" src="https://github.com/user-attachments/assets/4452ea33-40d2-4a9d-9e45-557a4847c451" />
  
  ## Maintenance Workflow
  <img width="1588" height="694" alt="image" src="https://github.com/user-attachments/assets/7600a10e-cc38-454b-b27e-7474e8f85890" />


## Workflow Highlights:

- Edge → MQTT → AWS RDS for real-time data ingestion
- AWS Step Functions orchestrate adaptive workflows using Choice State logic
- EventBridge triggers Lambda for workflow initiation
- SNS sends approval emails with Approve/Reject links
- API Gateway resumes workflow instantly upon approval

## Technologies Used
- AWS Services: Step Functions, EventBridge, Lambda, SNS, API Gateway
- Data Layer: AWS RDS (SQL Server)
- Messaging: MQTT for edge-to-cloud data flow
- Programming: Python for Lambda functions and workflow logic

## Business Impact
- Agile Operations: Workflows adapt in seconds based on machine status
- Compliance & Security: Callback pattern enforces human approvals mid-process
- Scalability: Cloud-native design supports multi-plant deployments
- Resilience: Workflow state maintained during approval wait, ensuring continuity

  ## Lambda Function Code

## Code Highlight: Check Machine Status Lambda
```python
def lambda_handler(event, context):
    conn = pymssql.connect(server=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, MachineStatus, QualityTrend, ProductionTarget, ProductionActual
        FROM MESData ORDER BY Timestamp DESC OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY
    """)
    row = cursor.fetchone()
    return {"MachineID": row[0], "MachineStatus": row[1], "QualityTrend": row[2]}
**Full script in adaptive-workflow folder.**
```
## Code Highlight: Create Maintenance Order Lambda

```python
order_id = f"MO_{int(datetime.now().timestamp())}"
cursor.execute("""
    INSERT INTO MaintenanceOrders (OrderID, MachineID, Status, CreatedAt)
    VALUES (%s, %s, %s, %s)
""", (order_id, machine_id, 'Created', datetime.now()))
**Full script in adaptive-workflow folder.**
```
## Code Highlight: Allocate Resources Lambda
```python
cursor.execute("SELECT TOP 1 ResourceID FROM Resources WHERE Status='Available' AND ResourceType='Technician'")
technician_id = cursor.fetchone()[0]
cursor.execute("SELECT TOP 1 ResourceID FROM Resources WHERE Status='Available' AND ResourceType='Equipment'")
tool_id = cursor.fetchone()[0]
**Full script in adaptive-workflow folder.**
```
