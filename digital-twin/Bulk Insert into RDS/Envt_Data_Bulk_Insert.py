import pyodbc
import random
from datetime import datetime, timedelta

# Database connection details
server = 'edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com'
database = 'TestDB'
username = 'admin'
password = 'Apriso2020'

# Connect to SQL Server
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

# Record IDs
record_ids = list(range(4006, 5006))

for record_id in record_ids:
    temperature = round(random.uniform(22.0, 35.0), 2)
    humidity = round(random.uniform(40.0, 70.0), 2)
    co2_level = round(random.uniform(400.0, 1200.0), 2)
    aqi = random.randint(50, 150)
    noise_level = round(random.uniform(65.0, 90.0), 2)
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))

    cursor.execute("""
        INSERT INTO MES_EnvironmentalData (RecordID, Temperature, Humidity, CO2Level, AQI, NoiseLevel, Timestamp, ProcessedFlag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (record_id, temperature, humidity, co2_level, aqi, noise_level, timestamp, 1))

conn.commit()
print(f"Inserted {len(record_ids)} rows into MES_EnvironmentalData.")
cursor.close()
conn.close()