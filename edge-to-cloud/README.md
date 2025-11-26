# Edge To Cloud

## Description
This POC demonstrates secure, real-time data flow between shop-floor machines and the cloud using a hybrid architecture. It combines MQTT for lightweight messaging and OPC UA for machine connectivity with RESTful APIs for structured, transactional data exchange between MES and enterprise systems.

## Architecture Diagram
<img width="938" height="568" alt="image" src="https://github.com/user-attachments/assets/1f0d84df-b230-404c-a66f-7722ca56a8e6" />
<img width="944" height="631" alt="image" src="https://github.com/user-attachments/assets/156f601f-f9c7-409d-9e25-38f0f1a71d1d" />

## Technologies Used
- Protocols: MQTT, OPC UA, RESTful Web API
- Messaging Broker: RabbitMQ
- Cloud Services: AWS EC2, AWS RDS (SQL Server)
- Programming: Python (Publisher & Subscriber scripts, REST API calls)
- Security: API Key authentication, HTTPS for REST API
- RESTful Web API for structured enterprise ↔ cloud integration

## Setup Instructions
- Configure RabbitMQ MQTT broker on AWS EC2.
- Deploy Python publisher and subscriber scripts for permanent MQTT connection.
- Set up REST API endpoint on EC2 for transactional data exchange.
- Connect to AWS RDS for data persistence.

## Business Impact
* Real-Time Visibility: Enables instant data exchange between edge devices and cloud systems.
* Structured Integration: REST API ensures secure, firewall-friendly communication with ERP, PLM, and QMS.
* Scalability: Supports multi-plant deployments with modular architecture.
* Foundation for Industry 4.0: Serves as the backbone for advanced MES capabilities like AI-driven analytics and Digital Twin integration.
* Operational Resilience: Maintains local control while providing global insights, even in low-connectivity environments.
