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
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

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
def random_delay(min_delay=3, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to type a prompt in ChatGPT's dialog box
def type_prompt_in_chatgpt(plant_name, retries=3, wait_time=10):
    prompt_text = (
        f"Provide the following specific data in strict JSON format for the plant '{plant_name}' and only these attributes:\n"
        "{{\n"
        "  'Seed Name': '{plant_name}'\n"
        "  'Temperature (2 m)': \n"
        "  'Precipitation': \n"
        "  'Soil Temperature (0 to 6 cm)': \n"
        "  'Soil Moisture (0-3 cm)': \n"
        "  'Sunshine Duration': \n"
        "  'Humidity': \n"
        "  'Soil Type': \n"
        "  'Soil pH' : \n"
        "  'Spacing' : \n"
        "  'Seed depth' :\n"
        "  'Hardiness zone' : \n"
        "  'Watering (per week)':\n"
        "}}\n"
        "Do not include any additional information or fields beyond the ones listed above."
        ""
    )

    for attempt in range(retries):
        try:
            print(f"Attempting to send prompt for '{plant_name}' (Attempt {attempt + 1}/{retries})...")
            # Wait for the input box to be visible and clickable
            input_box = WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located((By.ID, 'prompt-textarea'))
            )
            input_box.click()
            input_box.send_keys(prompt_text)
            random_delay()
            input_box.send_keys(Keys.RETURN)
            print(f"Prompt sent for '{plant_name}'.")
            return True
        except (StaleElementReferenceException, TimeoutException) as e:
            logging.error(f"Error sending prompt for '{plant_name}': {e}")
            print(f"Error sending prompt for '{plant_name}': {e}")
            if attempt == retries - 1:
                print(f"Failed to send prompt for '{plant_name}' after {retries} attempts. Stopping.")
                return False  # Stop further attempts if it fails after retries
            random_delay()

    return False

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

# Collect data iteratively and save only once at the end
all_collected_data = []
output_path = 'test-sheet.csv'  # Specify output file

for index, plant_name in enumerate(df['Names'], start=1):
    print(f"Processing plant {index}/{len(df['Names'])}: {plant_name}")

    # Attempt to type the prompt
    if not type_prompt_in_chatgpt(plant_name):  # If sending the prompt fails
        print(f"Stopping script as element not found for plant '{plant_name}'.")
        break  # Exit the loop if element cannot be interacted with

    random_delay()

    # Attempt to extract response
    response = extract_response()
    if response:
        all_collected_data.extend(response)

# Save all collected data at the end
if all_collected_data:
    # Save once at the end
    pd.DataFrame(all_collected_data).to_csv(output_path, index=False)
    print(f"All data saved to '{output_path}'.")
else:
    print("No data collected. Exiting.")

print("Script finished.") 
