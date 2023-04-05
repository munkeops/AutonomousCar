import json
import logging
import sys
from datetime
import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

vehicle_data = {}

def lambda_handler(event, context):
    global vehicle_data
    #TODO1: Get your data
    client.publish(
        topic=f"lambda/dump",
        payload=json.dumps(event),
    )
    
    if "vehicle_id" in event:
        vehicle_id = event['vehicle_id']
        if vehicle_id not in vehicle_data:
            vehicle_data[vehicle_id] = {
                "vehicle_id": vehicle_id,
                "co2_max": event['vehicle_CO2'],
                "timestep": event['timestep_time'],
            }

        #TODO2: Calculate max CO2 emission
        if event['vehicle_CO2'] > vehicle_data[vehicle_id]['co2_max']:
            vehicle_data[vehicle_id]['co2_max'] = event['vehicle_CO2']

        if event['vehicle_speed'] > vehicle_data[vehicle_id]['speed_max']:
            vehicle_data[vehicle_id]['speed_max'] = event['vehicle_speed']        

        #TODO3: Return the result
        client.publish(
            topic=f"emission/{vehicle_id}/results",
            payload=json.dumps(vehicle_data[vehicle_id]),
        )

    return