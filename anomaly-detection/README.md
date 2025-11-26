# AI Powered Anomaly Detection

## Description
This POC demonstrates how MES data can be leveraged for predictive analytics using machine learning. The goal is to detect anomalies in production processes proactively, reducing downtime and improving quality. The solution integrates AWS services for model training and automation, with Grafana for real-time visualization.

## Architecture Diagram
<img width="944" height="631" alt="image" src="https://github.com/user-attachments/assets/4b54bfb2-5eed-4d5c-8289-32b0090fc267" />

## Realtime Dashboard 
<img width="940" height="518" alt="image" src="https://github.com/user-attachments/assets/41b8983c-f4b1-4afa-9e49-1814060066ed" />

## Workflow:
- MES data stored in AWS RDS
- ML model trained using AWS SageMaker
- Automated anomaly detection via AWS Lambda
- Visualization using Grafana dashboards

## Technologies Used
- Cloud Services: AWS SageMaker, AWS Lambda, AWS RDS
- Visualization: Grafana OSS
- Programming: Python (Isolation Forest model, batch scripts)
- Automation: Windows Task Scheduler, Docker-based Lambda packaging

## Business Impact
- Proactive Quality Control: Detect anomalies before they impact production
- Reduced Downtime: Early alerts prevent costly stoppages
- Data-Driven Decisions: Real-time dashboards empower operators and managers
- Scalability: Cloud-native design supports multi-plant deployments
- Cost Efficiency: Serverless execution reduces infrastructure overhead

  ## Code Snipet
  
## Code Highlight: AI-Powered Anomaly Detection
```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Feature engineering
df['CycleTime'] = (df['EndTime'] - df['StartTime']).dt.total_seconds() / 60
df['DefectsRatio'] = df['Defects'] / df['QuantityProduced']
df['ProductionRate'] = df['QuantityProduced'] / df['CycleTime']

# Scale features
features = ['QuantityProduced', 'Defects', 'Temperature', 'Pressure', 'CycleTime', 'DefectsRatio', 'ProductionRate']
X_scaled = StandardScaler().fit_transform(df[features])

# Predict anomalies
model = IsolationForest(contamination=0.05)
model.fit(X_scaled)
df['AnomalyFlag'] = model.predict(X_scaled)
**Full script available in anomaly-detection folder.** 
```
## Code Highlight: Training Isolation Forest Model
```python
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib

# Feature engineering
df['CycleTime'] = (df['EndTime'] - df['StartTime']).dt.total_seconds() / 60
df['DefectsRatio'] = df['Defects'] / df['QuantityProduced']
df['ProductionRate'] = df['QuantityProduced'] / df['CycleTime']

# Scale features
features = ['QuantityProduced', 'Defects', 'Temperature', 'Pressure', 'CycleTime', 'DefectsRatio', 'ProductionRate']
X_scaled = StandardScaler().fit_transform(df[features])

# Train Isolation Forest model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_scaled)

# Save model
joblib.dump(model, "isolation_forest_model.pkl")

**Full script available in anomaly-detection folder.**
```



