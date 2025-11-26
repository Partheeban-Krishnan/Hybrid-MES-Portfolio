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

# Provided RecordIDs
record_ids = list(range(4006, 5006))  # Adjust based on your list

# Energy rate for cost calculation
energy_rate = 12.0  # currency per kWh

# Generate and insert data
for record_id in record_ids:
    energy_consumed = round(random.uniform(10.0, 20.0), 2)  # kWh
    power_peak = round(random.uniform(2.0, 5.0), 2)         # kW
    energy_cost = round(energy_consumed * energy_rate, 2)
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))  # last 24 hrs
    
    cursor.execute("""
        INSERT INTO MES_EnergyMetrics (RecordID, EnergyConsumed, PowerPeak, EnergyCost, Timestamp, ProcessedFlag)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (record_id, energy_consumed, power_peak, energy_cost, timestamp, 1))

# Commit changes
conn.commit()
print(f"Inserted {len(record_ids)} rows into MES_EnergyMetrics.")

# Close connection
cursor.close()
conn.close()