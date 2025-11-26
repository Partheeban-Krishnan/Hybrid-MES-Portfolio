import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine, text
from datetime import datetime
import logging
import sys
import os

# Setup logging
logging.basicConfig(filename="anomaly_detection_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

try:
    print("✅ Starting anomaly detection...")

    # Database connection details
    rds_host = 'edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com'
    db_name = 'testDB'
    username = 'admin'
    password = 'Apriso2020'

    # Create SQLAlchemy engine
    engine = create_engine(
        f"mssql+pyodbc://{username}:{password}@{rds_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    )

    # Load pre-trained model
    model_path = "isolation_forest_model.pkl"
    if not os.path.exists(model_path):
        logging.error(f"Model file not found: {model_path}")
        print("❌ Model file not found!")
        sys.exit(1)

    model = joblib.load(model_path)
    logging.info("Model loaded successfully.")
    print("✅ Model loaded successfully.")

    # Fetch unprocessed data
    query = """
    SELECT RecordID, QuantityProduced, Defects, Temperature, Pressure, StartTime, EndTime
    FROM MES_ProductionData
    WHERE ProcessedFlag = 0
    """
    df = pd.read_sql(query, engine)
    logging.info(f"Rows fetched for anomaly detection: {len(df)}")
    print(f"✅ Rows fetched: {len(df)}")

    if df.empty:
        logging.info("No new data to process.")
        print("ℹ No new data to process.")
        sys.exit(0)

    # Feature Engineering
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    df['EndTime'] = pd.to_datetime(df['EndTime'])
    df['CycleTime'] = (df['EndTime'] - df['StartTime']).dt.total_seconds() / 60
    df['DefectsRatio'] = df['Defects'] / df['QuantityProduced']
    df['ProductionRate'] = df['QuantityProduced'] / df['CycleTime']

    # Select features
    features = ['QuantityProduced', 'Defects', 'Temperature', 'Pressure', 'CycleTime', 'DefectsRatio', 'ProductionRate']
    X = df[features]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Predict anomalies
    df['AnomalyFlag'] = model.predict(X_scaled)  # -1 = anomaly, 1 = normal
    df['AnomalyScore'] = model.decision_function(X_scaled)

    # Prepare anomaly subset
    anomaly_df = df[df['AnomalyFlag'] == -1]
    print(f"⚠️ Anomalies detected: {len(anomaly_df)}")

    # Fetch existing anomaly IDs for NOT IN logic
    existing_ids_query = "SELECT RecordID FROM MES_Production_Anomalies"
    existing_ids_df = pd.read_sql(existing_ids_query, engine)
    existing_ids = set(existing_ids_df['RecordID'])

    # Insert anomalies and update ProcessedFlag
    model_name = 'IsolationForest'
    detection_time = datetime.now()
    inserted_count = 0
    skipped_count = 0

    with engine.begin() as conn:
        for _, row in anomaly_df.iterrows():
            record_id = int(row['RecordID'])
            if record_id not in existing_ids:  # ✅ NOT IN logic
                conn.execute(text("""
                    INSERT INTO MES_Production_Anomalies (RecordID, AnomalyFlag, AnomalyScore, ModelName, DetectionTime, ProcessedFlag)
                    VALUES (:RecordID, :AnomalyFlag, :AnomalyScore, :ModelName, :DetectionTime, 1)
                """), {
                    "RecordID": record_id,
                    "AnomalyFlag": int(row['AnomalyFlag']),
                    "AnomalyScore": float(row['AnomalyScore']),
                    "ModelName": model_name,
                    "DetectionTime": detection_time
                })
                inserted_count += 1
            else:
                skipped_count += 1

            # Update ProcessedFlag in MES_ProductionData
            conn.execute(text("""
                UPDATE MES_ProductionData
                SET ProcessedFlag = 1
                WHERE RecordID = :RecordID
            """), {"RecordID": record_id})

    # Summary output
    print("✅ Summary:")
    print(f"   Total anomalies detected: {len(anomaly_df)}")
    print(f"   Inserted into DB: {inserted_count}")
    print(f"   Skipped (already exists): {skipped_count}")

    logging.info(f"Anomalies detected: {len(anomaly_df)}")
    logging.info(f"Inserted: {inserted_count}, Skipped: {skipped_count}")
    logging.info("✅ Processing completed.")

except Exception as e:
    logging.error(f"Error occurred: {str(e)}")
    print(f"❌ Error occurred: {str(e)}")
    sys.exit(1)