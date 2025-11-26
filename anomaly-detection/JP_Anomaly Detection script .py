import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sqlalchemy import create_engine, text
from datetime import datetime

# 1. Create SQLAlchemy engine for SQL Server RDS
rds_host = 'edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com'
db_name = 'testDB'
username = 'admin'
password = 'Apriso2020'

engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{rds_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
)

# 2. Load all MES production data
query = """
SELECT RecordID, QuantityProduced, Defects, Temperature, Pressure, StartTime, EndTime
FROM MES_ProductionData
"""
df = pd.read_sql(query, engine)
print(f"✅ Rows fetched from MES_ProductionData: {len(df)}")

# 3. Feature Engineering
df['StartTime'] = pd.to_datetime(df['StartTime'])
df['EndTime'] = pd.to_datetime(df['EndTime'])
df['CycleTime'] = (df['EndTime'] - df['StartTime']).dt.total_seconds() / 60

# Derived metrics
df['DefectsRatio'] = df['Defects'] / df['QuantityProduced']
df['ProductionRate'] = df['QuantityProduced'] / df['CycleTime']

# Features
features = ['QuantityProduced', 'Defects', 'Temperature', 'Pressure', 'CycleTime', 'DefectsRatio', 'ProductionRate']
X = df[features]

# 4. Scale Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
df['AnomalyFlag'] = model.fit_predict(X_scaled)  # -1 = anomaly, 1 = normal
df['AnomalyScore'] = model.decision_function(X_scaled)


# Save the trained model for reuse
import joblib
joblib.dump(model, 'isolation_forest_model.pkl')
print("✅ Model saved successfully as isolation_forest_model.pkl")


# Count anomalies
anomaly_count = (df['AnomalyFlag'] == -1).sum()
print(f"✅ Anomalies detected: {anomaly_count}")

# 6. Insert anomalies into MES_Production_Anomalies table
model_name = 'IsolationForest'
detection_time = datetime.now()

with engine.begin() as conn:
    # Clear old anomalies
    conn.execute(text("TRUNCATE TABLE MES_Production_Anomalies"))
    
    # Insert only anomalies
    for index, row in df[df['AnomalyFlag'] == -1].iterrows():
        conn.execute(text("""
            INSERT INTO MES_Production_Anomalies (RecordID, AnomalyFlag, AnomalyScore, ModelName, DetectionTime)
            VALUES (:RecordID, :AnomalyFlag, :AnomalyScore, :ModelName, :DetectionTime)
        """), {
            "RecordID": int(row['RecordID']),
            "AnomalyFlag": int(row['AnomalyFlag']),
            "AnomalyScore": float(row['AnomalyScore']),
            "ModelName": model_name,
            "DetectionTime": detection_time
        })

print(f"✅ Anomalies stored in RDS successfully! Records inserted: {anomaly_count}")
