import boto3
import pymssql
import logging
from decimal import Decimal

# ---------------- CONFIG ----------------
workspace_id = "DigitalTwin"
entity_id = "96437eb2-4774-4e12-8e15-bed7bc943edf"  # Replace with actual Machine entity ID
component_name = "MAchineTimeSeries"
region = "ap-south-1"

rds_host = "edge-cloud-mes-db.clisu46igb60.ap-south-1.rds.amazonaws.com"
rds_user = "admin"
rds_password = "Apriso2020"
rds_db = "TestDB"

update_interval = 60  # seconds
log_file = "Timeseries_TwinMaker_Update.log"
# ----------------------------------------

logging.basicConfig(filename=log_file, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

client = boto3.client("iottwinmaker", region_name=region)

def convert_decimal(obj):
    return float(obj) if isinstance(obj, Decimal) else obj

def fetch_machine_ids():
    """Fetch all distinct MachineIDs from MES_ProductionData."""
    try:
        conn = pymssql.connect(server=rds_host, user=rds_user, password=rds_password, database=rds_db)
        cursor = conn.cursor(as_dict=True)
        cursor.execute("SELECT DISTINCT MachineID FROM MES_ProductionData")
        machines = [row['MachineID'] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return machines
    except Exception as e:
        logging.error(f"Error fetching MachineIDs: {e}")
        return []

def fetch_data(machine_id):
    """Fetch latest metrics for a given MachineID from all tables."""
    try:
        conn = pymssql.connect(server=rds_host, user=rds_user, password=rds_password, database=rds_db)
        cursor = conn.cursor(as_dict=True)

        cursor.execute("""
        SELECT TOP 1 Status, Temperature, Pressure, RecordID
        FROM MES_ProductionData WHERE MachineID = %s
        ORDER BY EndTime DESC
        """, (machine_id,))
        prod = cursor.fetchone()
        record_id = prod['RecordID'] if prod else None

        energy, env = None, None
        if record_id:
            cursor.execute("""
            SELECT TOP 1 EnergyConsumed, PowerPeak
            FROM MES_EnergyMetrics WHERE RecordID = %s
            ORDER BY Timestamp DESC
            """, (record_id,))
            energy = cursor.fetchone()

            cursor.execute("""
            SELECT TOP 1 Temperature AS EnvTemp, Humidity, CO2Level
            FROM MES_EnvironmentalData WHERE RecordID = %s
            ORDER BY Timestamp DESC
            """, (record_id,))
            env = cursor.fetchone()

        cursor.close()
        conn.close()
        return prod, energy, env
    except Exception as e:
        logging.error(f"Error fetching data for {machine_id}: {e}")
        return None, None, None

def update_twinmaker(machine_id, prod, energy, env):
    """Update TwinMaker entity properties for the selected machine."""
    if not prod:
        logging.warning(f"No production data for MachineID {machine_id}. Skipping update.")
        return

    update_payload = {
        "componentUpdates": {
            component_name: {
                "propertyUpdates": {
                    "MachineID": {"value": {"stringValue": machine_id}},
                    "Status": {"value": {"stringValue": prod['Status']}},
                    "MachineTemp": {"value": {"doubleValue": convert_decimal(prod['Temperature'])}},
                    "Pressure": {"value": {"doubleValue": convert_decimal(prod['Pressure'])}},
                    "EnergyConsumed": {"value": {"doubleValue": convert_decimal(energy['EnergyConsumed']) if energy else 0.0}},
                    "PowerPeak": {"value": {"doubleValue": convert_decimal(energy['PowerPeak']) if energy else 0.0}},
                    "EnvTemp": {"value": {"doubleValue": convert_decimal(env['EnvTemp']) if env else 0.0}},
                    "Humidity": {"value": {"doubleValue": convert_decimal(env['Humidity']) if env else 0.0}},
                    "CO2Level": {"value": {"doubleValue": convert_decimal(env['CO2Level']) if env else 0.0}}
                }
            }
        }
    }

    print(f"Updating entity {entity_id} for MachineID {machine_id} with payload:", update_payload)
    logging.info(f"Payload for MachineID {machine_id}: {update_payload}")

    try:
        response = client.update_entity(
            workspaceId=workspace_id,
            entityId=entity_id,
            componentUpdates=update_payload["componentUpdates"]
        )
        logging.info(f"Update successful for MachineID {machine_id}: {response['updateDateTime']}")
    except Exception as e:
        logging.error(f"Error updating TwinMaker entity for MachineID {machine_id}: {e}")

def main():
    logging.info("Starting TwinMaker dynamic machine update service...")
    machines = fetch_machine_ids()
    if not machines:
        logging.warning("No machines found. Exiting.")
        return

    for machine_id in machines:
        prod, energy, env = fetch_data(machine_id)
        update_twinmaker(machine_id, prod, energy, env)

if __name__ == "__main__":
    main()
