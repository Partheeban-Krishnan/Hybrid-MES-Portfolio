import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sqlalchemy import create_engine, text
from datetime import datetime
import joblib
import logging

# Setup logging
logging.basicConfig(filename="train_model_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

try:
    # Database connection details
    rds_host = 'edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com'
    db_name = 'testDB'
    username = 'admin'
    password = 'Apriso2020'

    # Create SQLAlchemy engine
    engine = create_engine(
        f"mssql+pyodbc://{username}:{password}@{rds_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    )

    # Load historical MES production data
    query = """
    SELECT RecordID, QuantityProduced, Defects, Temperature, Pressure, StartTime, EndTime
    FROM MES_ProductionData
    """
    df = pd.read_sql(query, engine)
    logging.info(f"Rows fetched: {len(df)}")

    # Feature Engineering
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    df['EndTime'] = pd.to_datetime(df['EndTime'])
    df['CycleTime'] = (df['EndTime'] - df['StartTime']).dt.total_seconds() / 60
    df['DefectsRatio'] = df['Defects'] / df['QuantityProduced']
    df['ProductionRate'] = df['QuantityProduced'] / df['CycleTime']

    # Select features
    features = ['QuantityProduced', 'Defects', 'Temperature', 'Pressure', 'CycleTime', 'DefectsRatio', 'ProductionRate']
    X = df[features]

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_scaled)

    # Save model
    joblib.dump(model, "isolation_forest_model.pkl")
    logging.info("Model trained and saved successfully as isolation_forest_model.pkl")

except Exception as e:
    logging.error(f"Error occurred: {str(e)}")
    print("❌ Error occurred during training. Check train_model_log.txt for details.")
else:
    print("✅ Model training completed and saved as isolation_forest_model.pkl")