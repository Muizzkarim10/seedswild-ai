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
        "  'Temperature (2 m)': '24°C',\n"  # Single value for temperature
        "  'Precipitation': '400 mm',\n"    # Single value for precipitation
        "  'Soil Temperature (0 to 6 cm)': '15°C',\n"  # Single value for soil temperature
        "  'Soil Moisture (0-3 cm)': '70%',\n"  # Single value for soil moisture
        "  'Sunshine Duration': '7 hours',\n"  # Single value for sunshine duration
        "  'Humidity': '65%',\n"  # Single value for humidity
        "  'Soil Type': ['Loam', 'Sandy Loam', 'Clay Loam'],\n"
        "  'Watering (per week)': '30 mm '\n"  # Single value for watering
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

    except Exception as e:
        logging.error(f"Failed to type prompt in ChatGPT for {plant_name}: {e}")
        print(f"Failed to type prompt in ChatGPT for {plant_name}: {e}")

# Function to extract the response
def extract_response():
    try:
        response_elements = driver.find_elements(By.CSS_SELECTOR, 'div.overflow-y-auto.p-4 code.hljs.language-json')
        responses = []

        for response_element in response_elements:
            response_text = response_element.text
            plant_data = json.loads(response_text)
            responses.append(plant_data)

        return responses

    except Exception as e:
        logging.error(f"Failed to extract responses: {e}")
        print(f"Failed to extract responses: {e}")
        return []

# Collect all responses for all plants
all_collected_data = []

# Iterate over the plant names in the CSV and send the prompts
for plant_name in df['Names']:
    type_prompt_in_chatgpt(plant_name)
    random_delay()  # Random delay between requests to avoid rate limiting

# Wait for all responses to be received
# time.sleep(5)  # Adjust time based on your observation of response speed

# Extract all responses after all prompts are sent
collected_data = extract_response()

# Check if responses were extracted and append to the all collected data list
if collected_data:
    all_collected_data.extend(collected_data)

# Save the data after all responses are received
if all_collected_data:
    output_df = pd.DataFrame(all_collected_data)
    output_path = 'plant_data.csv'  # Absolute path for consistency
    output_df.to_csv(output_path, index=False)
    print(f"All data saved to '{output_path}'.")

print("Script finished.")
