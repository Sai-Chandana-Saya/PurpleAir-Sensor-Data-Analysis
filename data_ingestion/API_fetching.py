import requests
import os
import csv
from datetime import datetime, timedelta, timezone

# Constants
API_KEY = "79C25470-743B-11F0-AF66-42010A800028"
SENSOR_INDEX = 256923  # Los Angeles Ecovillage sensor index
OUTPUT_DIR = r"D:\Project\notebooks"

def fetch_sensor_history(sensor_index):
    """Fetch historical data for a specific sensor."""
    # Calculate time range (last 3 months)
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(days=90)
    
    # API endpoint - corrected URL format
    url = f"https://api.purpleair.com/v1/sensors/{sensor_index}/history"
    
    # Parameters - simplified and corrected
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
        
        data = response.json()
        if not data.get('data'):
            print("No data returned from API")
            return None
            
        # Map fields to sensor data
        fields = data['fields']
        return [dict(zip(fields, sensor)) for sensor in data['data']]
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response content: {e.response.text}")
        return None

def save_to_csv(sensors, filepath):
    """Saves sensor data to a CSV file."""
    if not sensors:
        print("No sensor data to save.")
        return
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Write to CSV
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sensors[0].keys())
        writer.writeheader()
        writer.writerows(sensors)
    
    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    # Fetch sensor history
    sensor_data = fetch_sensor_history(SENSOR_INDEX)
    
    if sensor_data:
        print(f"Successfully fetched data for sensor {SENSOR_INDEX}")
        
        # Save to CSV
        csv_filename = f"purpleair_sensor_{SENSOR_INDEX}_data.csv"
        csv_path = os.path.join(OUTPUT_DIR, csv_filename)
        save_to_csv(sensor_data, csv_path)
    else:
        print(f"Failed to fetch data for sensor {SENSOR_INDEX}")