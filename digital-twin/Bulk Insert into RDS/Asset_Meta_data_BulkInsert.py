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

# Example MachineIDs from MES_ProductionData
machine_ids = ['MCH001', 'MCH002', 'MCH003', 'MCH004', 'MCH005', 'MCH006', 'MCH007', 'MCH008', 'MCH009', 'MCH010']

# Sample data pools
asset_types = ["Machine", "Robot", "Conveyor", "Sensor"]
locations = ["Zone A", "Zone B", "Zone C", "Zone D"]
manufacturers = ["KraussMaffei", "DMG Mori", "ABB", "Siemens", "Fanuc"]
models = ["IMM-450", "NLX-2500", "IRB-6700", "S7-1500", "LR Mate 200iD"]
criticality_levels = ["High", "Medium", "Low"]

for machine_id in machine_ids:
    asset_name = f"Asset_{machine_id}"
    asset_type = random.choice(asset_types)
    location = random.choice(locations)
    manufacturer = random.choice(manufacturers)
    model_number = random.choice(models)
    install_date = datetime.now() - timedelta(days=random.randint(365, 2000))  # 1-5 years old
    capacity = random.randint(100, 1000)
    maintenance_interval = random.choice([30, 45, 60])  # days
    criticality = random.choice(criticality_levels)
    status = "Active"
    timestamp = datetime.now()

    cursor.execute("""
        INSERT INTO MES_AssetMetadata (MachineID, AssetName, AssetType, Location, Manufacturer, ModelNumber, InstallDate, Capacity, MaintenanceInterval, Criticality, Status, Timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (machine_id, asset_name, asset_type, location, manufacturer, model_number, install_date, capacity, maintenance_interval, criticality, status, timestamp))

conn.commit()
print(f"Inserted {len(machine_ids)} rows into MES_AssetMetadata.")
cursor.close()
conn.close()