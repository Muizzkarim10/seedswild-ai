import subprocess
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
from selenium.common.exceptions import StaleElementReferenceException

# Load the CSV file to fetch plant names
csv_file_path = "sample.csv"  # Update to absolute path if needed
df = pd.read_csv(csv_file_path)

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='script_debug.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Start Chrome with remote debugging
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
remote_debugging_port = '9222'
user_data_dir = r'C:\Users\Muizz\AppData\Local\Google\Chrome\User Data\Profile 2'

cmd = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port} --user-data-dir="{user_data_dir}"'
process = subprocess.Popen(cmd, shell=True)
print("Chrome launched with remote debugging.")

# Prompt user to manually log in and navigate to ChatGPT
input("Press Enter after you have navigated to the ChatGPT chat box and logged in. Make sure Chrome is still open...")

# Configure Selenium to attach to the existing Chrome session
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

# Try to connect to the existing Chrome session
try:
    print("Attempting to connect to Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome. Current page title: " + driver.title)
except Exception as e:
    logging.error(f"Failed to connect to Chrome: {e}")
    print(f"Failed to connect to Chrome: {e}")
    exit()

# Function to add random delay
def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to type a prompt in ChatGPT's dialog box
def type_prompt_in_chatgpt(plant_name):
    prompt_text = (
        f"Provide the following specific data in strict JSON format for the plant '{plant_name}' and only these attributes:\n"
        "{{\n"
        "  'Seed Name': '{plant_name}',\n"
        "  'Temperature (2 m)': '18-29°C',\n"
        "  'Precipitation': '300-500 mm',\n"
        "  'Soil Temperature (0 to 6 cm)': '12-18°C',\n"
        "  'Soil Moisture (0-3 cm)': '60-80%',\n"
        "  'Sunshine Duration': '6-8 hours',\n"
        "  'Humidity': '60-75%',\n"
        "  'Soil Type': ['Loam', 'Sandy Loam', 'Clay Loam'],\n"
        "  'Watering': '25-35 mm per week'\n"
        "}}\n"
        "Do not include any additional information or fields beyond the ones listed above."
    )

    try:
        print(f"Locating the input box for plant: {plant_name}...")

        # Wait until the input box is clickable and then get the element again if stale
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'prompt-textarea'))
        )

        try:
            input_box.click()
            input_box.send_keys(prompt_text)
            random_delay()  # Random delay before sending the prompt
            input_box.send_keys(Keys.RETURN)  # Simulate pressing 'Enter' to send the message
            print(f"Prompt sent to ChatGPT for {plant_name}.")
        except StaleElementReferenceException:
            print(f"Stale element reference encountered for {plant_name}, retrying...")
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'prompt-textarea'))
            )
            input_box.click()
            input_box.send_keys(prompt_text)
            random_delay()
            input_box.send_keys(Keys.RETURN)
            print(f"Prompt sent after retry for {plant_name}.")

        # Wait for the response (adjust this delay as needed)
        time.sleep(random.uniform(5, 10))  # Adjust if necessary
        return plant_name

    except Exception as e:
        logging.error(f"Failed to type prompt in ChatGPT for {plant_name}: {e}")
        print(f"Failed to type prompt in ChatGPT for {plant_name}: {e}")

# Function to extract the response
def extract_responses():
    try:
        # Wait for all elements with the JSON data
        response_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.overflow-y-auto.p-4 code.hljs.language-json'))
        )

        plant_data_list = []
        for response_element in response_elements:
            response_text = response_element.text

            # Parse the JSON response
            plant_data = json.loads(response_text)
            if plant_data:
                formatted_data = {
                    "Seed Name": plant_data.get("Seed Name", ""),
                    "Temperature (2 m)": plant_data.get("Temperature (2 m)", ""),
                    "Precipitation": plant_data.get("Precipitation", ""),
                    "Soil Temperature (0 to 6 cm)": plant_data.get("Soil Temperature (0 to 6 cm)", ""),
                    "Soil Moisture (0-3 cm)": plant_data.get("Soil Moisture (0-3 cm)", ""),
                    "Sunshine Duration": plant_data.get("Sunshine Duration", ""),
                    "Humidity": plant_data.get("Humidity", ""),
                    "Soil Type": plant_data.get("Soil Type", ""),
                    "Watering": plant_data.get("Watering", "")
                }
                plant_data_list.append(formatted_data)

        return plant_data_list

    except Exception as e:
        logging.error(f"Failed to extract responses: {e}")
        print(f"Failed to extract responses: {e}")
        return []

# Collect all responses
collected_data = []

# Check if the CSV file already exists
output_path = 'plant_data.csv'  # Absolute path for consistency
try:
    existing_data = pd.read_csv(output_path)
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=["Seed Name", "Temperature (2 m)", "Precipitation", "Soil Temperature (0 to 6 cm)",
                                          "Soil Moisture (0-3 cm)", "Sunshine Duration", "Humidity", "Soil Type", "Watering"])

# Iterate over the plant names in the CSV and send the prompts
for plant_name in df['Names']:
    type_prompt_in_chatgpt(plant_name)
    time.sleep(random.uniform(2, 5))  # Random delay between requests to avoid rate limiting

    # Extract the responses after sending the prompt
    plant_data_list = extract_responses()

    # Add the extracted data to the collected list if not already in the CSV
    if plant_data_list:
        for plant_data in plant_data_list:
            if not existing_data[existing_data["Seed Name"] == plant_data["Seed Name"]].empty:
                print(f"Data for {plant_data['Seed Name']} already exists. Skipping...")
            else:
                collected_data.append(plant_data)

        # Save the new data to CSV
        if collected_data:
            output_df = pd.DataFrame(collected_data)
            output_df = pd.concat([existing_data, output_df], ignore_index=True)  # Append new data to existing
            output_df.to_csv(output_path, index=False)
            print(f"Data saved to '{output_path}'")

print("All data processed and saved.")
