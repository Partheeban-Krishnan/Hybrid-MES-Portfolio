# Adaptive Workflow & Human-in-the-Loop Automation

## Description
This POC demonstrates how MES workflows can be transformed from static processes into adaptive, event-driven workflows that respond dynamically to machine status. It incorporates Human-in-the-Loop (HIL) approvals for critical events, ensuring compliance and security while maintaining agility.

## Architecture Diagram
<img width="940" height="627" alt="image" src="https://github.com/user-attachments/assets/ce8bb93e-01b0-475b-bc3d-70522fba7148" />

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
