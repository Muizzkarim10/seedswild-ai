import requests
import pandas as pd
import time

# API details
API_KEY = "[REDACTED]"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Load plant names from the CSV file
plants_df = pd.read_csv("final.csv")  # Use the actual path to your CSV file
plant_names = plants_df.iloc[:, 0].tolist()  # Get the first column as a list of plant names

# Default location (latitude, longitude) - adjust based on a regional assumption
default_lat = 35.88  # Replace with approximate latitude for your area
default_lon = 74.49  # Replace with approximate longitude for your area

# Initialize an empty list to store the fetched data
data = []

# Function to fetch data from OpenWeatherMap API
def fetch_weather_data(lat, lon):
    try:
        # Prepare the parameters for the API request
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"  # Use metric system for Celsius
        }
        # Send request to the API
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for failed requests
        weather = response.json()
        
        # Extract required data
        temperature = weather["main"]["temp"]
        soil_temp = temperature - 2  # Mock adjustment for soil temperature
        precipitation = weather.get("rain", {}).get("1h", 0)  # mm in last hour
        humidity = weather["main"]["humidity"]
        sunshine_duration = weather["sys"]["sunrise"] - weather["sys"]["sunset"]  # Mock value

        # Return data as a dictionary
        return {
            "Temperature": temperature,
            "Soil_Temperature": soil_temp,
            "Precipitation": precipitation,
            "Humidity": humidity,
            "Sunshine_Duration": abs(sunshine_duration),  # Duration in seconds (mock value)
        }
    except Exception as e:
        print(f"Error fetching data for lat={lat}, lon={lon}: {e}")
        return None

# Fetch data for each plant using the default location
for plant_name in plant_names:
    weather_data = fetch_weather_data(default_lat, default_lon)
    if weather_data:
        weather_data["Plant_Name"] = plant_name
        data.append(weather_data)
        time.sleep(1)  # Pause to avoid hitting rate limits

# Create a DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("plant_weather_data.csv", index=False)

print("Data saved to plant_weather_data.csv")
