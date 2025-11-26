# Hybrid MES Portfolio – Advanced Use Cases
### Hybrid-mes,Manufacturing-Execution-System,Industry-4.0,edge-computing,cloud-integration,IIOT,AI/ML,MQTT,OPC-UA,AWS,Digital-twin,Predictive-Maintenance,Grafana,Apache-kafka,Rest API,adaptive-workflow,Smart-Manufacturing

## Introduction
This repository contains hands-on Proof-of-Concepts (POCs) exploring next-generation Hybrid MES architectures aligned with Industry 4.0 principles.

### POCs Included
- [Digital Twin with Real-Time Monitoring](digital-twin/README.md)
- [AI-Powered Anomaly Detection](anomaly-detection/README.md)
- [Adaptive Workflow & Human-in-the-Loop](adaptive-workflow/README.md)
- [Edge-to-Cloud Integration](edge-to-cloud/README.md)


## Tech Stack
**AWS Services**
- EC2 (Cloud hosting for MES components)
- RDS (SQL Server) (Data storage for MES production and quality data)
- Lambda (Serverless execution for anomaly detection and workflows)
- Step Functions (Adaptive workflows & orchestration)
- SNS (Notifications & Human-in-the-Loop approvals)
- EventBridge (Event-driven triggers)
- API Gateway (RESTful API integration)
- IoT TwinMaker (Digital Twin visualization)
- S3 (Storage for models and assets)
- SageMaker (AI/ML model training and retraining)

**Messaging & Integration**
- RabbitMQ (MQTT) (Edge-to-cloud real-time messaging)
- OPC UA (Edge connectivity for machine data)
- RESTful Web API (Enterprise ↔ Cloud integration)
  
**Data & Visualization**
- Grafana OSS (Dashboards for MES KPIs, anomaly trends, workflow status)
- Neo4j + PyVis (Graph-based machine relationships for Digital Twin)

**Machine Learning**
- Isolation Forest (Anomaly detection)
- Python (scikit-learn, pandas) for model development
- Docker (Packaging Lambda functions)
  
**Automation**
- Windows Task Scheduler (Periodic anomaly detection jobs)

**Programming Languages**
- Python (Scripts for MQTT, REST API, ML models)
- Flask (Web services for visualization and streaming)
## Repository Structure
```
hybrid-mes-portfolio/
├── README.md
├── edge-to-cloud/
├── anomaly-detection/
├── adaptive-workflow/
├── digital-twin/
└── diagrams/
```

## How to Use
- Add architecture diagrams in `diagrams/`
- Update each POC folder with code and documentation.
