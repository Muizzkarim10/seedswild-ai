import requests
import json
import csv
from datetime import datetime

# Input CSV file and output file paths
input_csv_file = 'sample.csv'  # Input file with plant names
output_csv_file = 'plant_data.csv'  # Output file to save the plant data
success_log_file = 'success_log.txt'  # Log file for successful operations
error_log_file = 'error_log.txt'  # Log file for unsuccessful operations

# API endpoint
url = "http://localhost:11434/api/generate"

# Function to fetch data for a given plant name
def fetch_data_for_plant(plant_name):
    data = {
        "model": "llama3",
        "prompt": f"Provide the following data for {plant_name}: temperature, soil temperature, precipitation, soil moisture, sunshine duration, and humidity. Return data in JSON format.",
        "stream": False
    }
    
    response = requests.post(url, json=data)

    try:
        json_response = response.json()
        if 'response' in json_response:
            # Extracting the JSON data from the response
            response_text = json_response['response']
            start_index = response_text.find("```") + 3  # Start after the first ```
            end_index = response_text.rfind("```")  # End before the last ```

            # If valid indices are found, extract and parse the JSON
            if start_index != -1 and end_index != -1 and end_index > start_index:
                inner_json_str = response_text[start_index:end_index].strip()
                return json.loads(inner_json_str)
            else:
                return None  # Return None if JSON extraction fails
        else:
            return None  # Return None if the response structure is unexpected
    except (json.JSONDecodeError, ValueError):
        return None  # Return None if there's a JSON parsing error

# Initialize output CSV with headers if not exists
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as out_csv:
    fieldnames = ['Name', 'Temperature', 'Soil Temperature', 'Precipitation', 'Soil Moisture', 'Sunshine Duration', 'Humidity']
    writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
    writer.writeheader()  # Write headers only once

# Read plant names from input CSV and process in real-time
with open(input_csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Process each plant name and save data immediately
    for row in reader:
        plant_name = row['Names']  # Adjust column name as necessary
        plant_data = fetch_data_for_plant(plant_name)

        if plant_data:
            # Ensure plant_data is a dictionary and not a list
            if isinstance(plant_data, dict):
                # Write data to output CSV immediately
                with open(output_csv_file, mode='a', newline='', encoding='utf-8') as out_csv:
                    writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
                    writer.writerow({
                        'Name': plant_name,
                        'Temperature': plant_data.get('temperature', {}).get('average_high', 'N/A'),  # Default to 'N/A'
                        'Soil Temperature': plant_data.get('soil_temperature', {}).get('average_daytime', 'N/A'),  # Default to 'N/A'
                        'Precipitation': plant_data.get('precipitation', {}).get('monthly_average', 'N/A'),  # Default to 'N/A'
                        'Soil Moisture': plant_data.get('soil_moisture', {}).get('optimal_range', 'N/A'),  # Default to 'N/A'
                        'Sunshine Duration': plant_data.get('sunshine_duration', {}).get('average_daily', 'N/A'),  # Default to 'N/A'
                        'Humidity': plant_data.get('humidity', {}).get('average_relative_humidity', 'N/A')  # Default to 'N/A'
                    })
                
                # Log the successful operation immediately
                with open(success_log_file, mode='a', encoding='utf-8') as success_log:
                    success_log.write(f"{datetime.now()} - Retrieved data for {plant_name} and saved to CSV\n")
                
            else:
                # Log the error if plant_data is not a dictionary
                with open(error_log_file, mode='a', encoding='utf-8') as error_log:
                    error_log.write(f"{datetime.now()} - Data for {plant_name} returned unexpected structure: {plant_data}\n")
                
        else:
            # Log the error if data could not be retrieved
            with open(error_log_file, mode='a', encoding='utf-8') as error_log:
                error_log.write(f"{datetime.now()} - Data for {plant_name} could not be retrieved.\n")
