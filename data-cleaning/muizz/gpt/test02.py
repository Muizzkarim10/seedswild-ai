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
csv_file_path = "sample.csv"  # Update the path to your CSV file
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
    # Construct the prompt for ChatGPT dynamically based on the plant name
    prompt_text = (
        f"Provide accurate data in JSON format for the plant '{plant_name}' covering only the following attributes: "
        "{\n"
        "  'Seed Name': '{plant_name}',\n"
        "  'Temperature (2 m)': '18-29°C',\n"
        "  'Precipitation': '300-500 mm',\n"
        "  'Soil Temperature (0 to 6 cm)': '12-18°C',\n"
        "  'Soil Moisture (0-3 cm)': '60-80%',\n"
        "  'Sunshine Duration': '6-8 hours',\n"
        "  'Humidity': '60-75%',\n"
        "  'Soil Type': ['Loam', 'Sandy Loam', 'Clay Loam'],\n"
        "  'Watering': '25-35 mm per week'\n"
        "}\n"
        "Do not include any other details or information about the plant. "
        "Ensure the data is in JSON format, strictly matching these fields, and no other attributes or details."
    )

    try:
        print(f"Locating the input box for plant: {plant_name}...")
        
        # Wait until the input box is clickable and then get the element again if stale
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'prompt-textarea'))
        )
        
        # In case of a stale element reference, re-locate the element
        try:
            input_box.click()
            input_box.send_keys(prompt_text)
            random_delay()  # Random delay before sending the prompt
            input_box.send_keys(Keys.RETURN)  # Simulate pressing 'Enter' to send the message
            print(f"Prompt sent to ChatGPT for {plant_name}.")
        except StaleElementReferenceException:
            print(f"Stale element reference encountered for {plant_name}, retrying to find the element...")
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'prompt-textarea'))
            )
            input_box.click()
            input_box.send_keys(prompt_text)
            random_delay()
            input_box.send_keys(Keys.RETURN)
            print(f"Prompt sent after retry for {plant_name}.")
        
    except Exception as e:
        logging.error(f"Failed to type prompt in ChatGPT for {plant_name}: {e}")
        print(f"Failed to type prompt in ChatGPT for {plant_name}: {e}")
        print("Make sure the correct element selector is used and that the input box is interactable.")

# Iterate over the plant names in the CSV and send the prompts
for plant_name in df['Names']:
    type_prompt_in_chatgpt(plant_name)
    time.sleep(random.uniform(2, 5))  # Random delay between requests to avoid rate limiting
