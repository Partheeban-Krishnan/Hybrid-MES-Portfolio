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

maintenance_types = ["Planned", "Unplanned"]
issues = ["Bearing wear", "Sensor fault", "Hydraulic leak", "Electrical short", "Software error"]
actions = ["Replaced bearing", "Calibrated sensor", "Fixed leak", "Rewired circuit", "Updated software"]

for record_id in record_ids:
    maintenance_type = random.choice(maintenance_types)
    issue_description = random.choice(issues)
    action_taken = random.choice(actions)
    start_time = datetime.now() - timedelta(days=random.randint(1, 7), hours=random.randint(0, 12))
    end_time = start_time + timedelta(hours=random.randint(1, 4))
    technician_id = f"T{random.randint(100, 999)}"
    cost = round(random.uniform(100.0, 500.0), 2)
    status = "Completed"
    timestamp = datetime.now()

    cursor.execute("""
        INSERT INTO MES_MaintenanceLogs (RecordID, MaintenanceType, IssueDescription, ActionTaken, StartTime, EndTime, TechnicianID, Cost, Status, Timestamp, ProcessedFlag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (record_id, maintenance_type, issue_description, action_taken, start_time, end_time, technician_id, cost, status, timestamp, 1))

conn.commit()
print(f"Inserted {len(record_ids)} rows into MES_MaintenanceLogs.")
cursor.close()
conn.close()
