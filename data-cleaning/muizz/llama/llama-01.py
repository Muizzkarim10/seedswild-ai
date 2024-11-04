import requests
import json
import csv
from datetime import datetime

# Input CSV file and output file paths
input_csv_file = 'sample.csv'  # Input file with plant names
output_csv_file = 'plant-data.csv'  # Output file to save the plant data
success_log_file = 'success_log.txt'  # Log file for successful operations
error_log_file = 'error_log.txt'  # Log file for unsuccessful operations

# API endpoint
url = "http://localhost:11434/api/generate"

# Define the attributes structure for the prompt
attributes = {
    "Seed Name": "abc",
    "Temperature (2 m)": "X-Y",
    "Precipitation": "a-b",
    "Soil Temperature (0 to 6 cm)": "X-Y",
    "Soil Moisture (0-3 cm)": "a-b",
    "Sunshine Duration": "a-b",
    "Humidity": "a-b",
    "Soil Type": ["abc", "abc", "abc"],
    "Watering": "X",
}

# Function to fetch data for a given plant name
def fetch_data_for_plant(plant_name):
    data = {
        "model": "llama3",
        "prompt": (
            f"Provide accurate data in JSON format for {plant_name} covering cultivation, alerts, and recommendations, "
            f"with the following attributes: {json.dumps(attributes, indent=2)}. "
            "Ensure all attributes are present, strictly numeric where specified, and exclude units in the response."
        ),
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        json_response = response.json()
        if 'response' in json_response:
            response_text = json_response['response']
            start_index = response_text.find("{")
            end_index = response_text.rfind("}") + 1
            
            if start_index != -1 and end_index != -1:
                inner_json_str = response_text[start_index:end_index].strip()
                return json.loads(inner_json_str)
        return None  # Return None if the response structure is unexpected
    except (requests.RequestException, json.JSONDecodeError, ValueError) as e:
        log_error(plant_name, str(e))
        return None

def log_success(plant_name):
    """Log successful data retrieval."""
    with open(success_log_file, mode='a', encoding='utf-8') as success_log:
        success_log.write(f"{datetime.now()} - Data retrieved and saved for {plant_name}\n")

def log_error(plant_name, error_message):
    """Log errors encountered during data retrieval."""
    with open(error_log_file, mode='a', encoding='utf-8') as error_log:
        error_log.write(f"{datetime.now()} - Error fetching data for {plant_name}: {error_message}\n")

# Read existing plant names from the output CSV file
existing_names = set()
try:
    with open(output_csv_file, mode='r', newline='', encoding='utf-8') as out_csv:
        reader = csv.DictReader(out_csv)
        for row in reader:
            existing_names.add(row['Name'])
except FileNotFoundError:
    pass  # The file does not exist yet, so no existing names

# Prepare output CSV with headers if not exists
with open(output_csv_file, mode='a', newline='', encoding='utf-8') as out_csv:
    fieldnames = ['Name', 'Seed Name', 'Temperature (2 m)', 'Precipitation',
                  'Soil Temperature (0 to 6 cm)', 'Soil Moisture (0-3 cm)',
                  'Sunshine Duration', 'Humidity', 'Soil Type', 'Watering']
    writer = csv.DictWriter(out_csv, fieldnames=fieldnames)

    if out_csv.tell() == 0:  # Write headers only if the file was empty
        writer.writeheader()

# Process plant names from input CSV
with open(input_csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        plant_name = row['Names']
        if plant_name in existing_names:
            continue  # Skip if the plant name already exists

        plant_data = fetch_data_for_plant(plant_name)

        if plant_data and isinstance(plant_data, dict):
            # Prepare row data with fetched information
            row_data = {'Name': plant_name}
            for field in fieldnames[1:]:  # Skip 'Name'
                row_data[field] = plant_data.get(field, None)  # Default to None if key is missing
            
            # Write to output CSV
            with open(output_csv_file, mode='a', newline='', encoding='utf-8') as out_csv:
                writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
                writer.writerow(row_data)

            # Log success
            log_success(plant_name)
        else:
            # Log error for missing or invalid data
            log_error(plant_name, "Failed to retrieve valid data")

