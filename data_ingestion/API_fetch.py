import requests
import os
import csv
from datetime import datetime, timedelta, timezone


# Constants
API_KEY = "79C25470-743B-11F0-AF66-42010A800028"
SENSOR_INDEX = 256923  # California sensor index
OUTPUT_DIR = r"D:\Project\notebooks"

current_time = datetime.now(timezone.utc)
start_time = current_time - timedelta(days=90)

url = url = f"https://api.purpleair.com/v1/sensors/{SENSOR_INDEX}/history/csv"

params = {
        "start_timestamp": start_time.isoformat(),
        "end_timestamp": current_time.isoformat(),
        "average": 30,  # 30-minute averages
        "fields": "pm2.5_atm,pm2.5_atm_a,pm2.5_atm_b,temperature,humidity,pressure"
    }

try:
    response = requests.get(
        url,
        headers={"X-API-Key": API_KEY}, 
        params=params,
        timeout=30
    )
    response.raise_for_status()

    data = response.text

    if not data:
            print("No data returned from API")
    
    ## Save the data to a CSV file
    filepath = os.path.join(OUTPUT_DIR, f"Puple_air_sensor_data.csv")

    with open(filepath,'w') as csvfile:
            csvfile.write(data)

    
    print(f"Data saved to {filepath}")
        

except requests.exceptions.RequestException as e:
    print(f"API Error: {e}")



    
    