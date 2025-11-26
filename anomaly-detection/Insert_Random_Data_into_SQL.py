import pyodbc
import random
from datetime import datetime, timedelta

# RDS Connection Details
server = 'edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com'  # e.g., mydb.xxxxxxx.us-east-1.rds.amazonaws.com
database = 'TestDB'
username = 'admin'
password = 'Apriso2020'
driver = '{ODBC Driver 17 for SQL Server}'  # Ensure this driver is installed on EC2

# Connect to RDS
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

# Function to generate random datetime within a range
def random_datetime(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

# Data generation parameters
machines = ['MCH001', 'MCH002', 'MCH003']
products = ['PRD1001', 'PRD1002', 'PRD1003', 'PRD1004', 'PRD1005']
shifts = ['A', 'B', 'C']
status = 'Completed'

start_range = datetime(2025, 11, 1, 0, 0, 0)
end_range = datetime(2025, 11, 6, 23, 59, 59)

# Generate and insert 2000 records
for i in range(2000):
    machine_id = random.choice(machines)
    product_code = random.choice(products)
    shift = random.choice(shifts)
    operator_id = f'OP{random.randint(100, 300)}'
    start_time = random_datetime(start_range, end_range)
    end_time = start_time + timedelta(hours=random.randint(1, 8))  # 1-8 hour duration
    quantity_produced = random.randint(400, 1000)
    defects = random.randint(0, 20)
    temperature = round(random.uniform(70.0, 90.0), 2)
    pressure = round(random.uniform(1.0, 1.5), 2)

    cursor.execute("""
        INSERT INTO MES_ProductionData (MachineID, ProductCode, Shift, OperatorID, StartTime, EndTime, QuantityProduced, Defects, Temperature, Pressure, Status,ProcessedFlag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,0)
    """, (machine_id, product_code, shift, operator_id, start_time, end_time, quantity_produced, defects, temperature, pressure, status))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ Successfully inserted 2000 records into MES_ProductionData!")