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

csv_file_path = "sample.csv"
df = pd.read_csv(csv_file_path)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
remote_debugging_port = '9222'
user_data_dir = r'C:\Users\Muizz\AppData\Local\Google\Chrome\User Data\Profile 3'

cmd = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port} --user-data-dir="{user_data_dir}"'
process = subprocess.Popen(cmd, shell=True)
print("Chrome launched with remote debugging.")

input("Press Enter after you have navigated to the ChatGPT chat box and logged in. Make sure Chrome is still open...")

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

try:
    print("Attempting to connect to Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome. Current page title: " + driver.title)
except Exception as e:
    logging.error(f"Failed to connect to Chrome: {e}")
    print(f"Failed to connect to Chrome: {e}")
    exit()

def random_delay(min_delay=3, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

def type_prompt_in_chatgpt(plant_name, retries=2, wait_time=5):
    prompt_text = (
        f"Plant name: {plant_name}"
    )


    for attempt in range(retries):
        try:
            print(f"Attempting to send prompt for '{plant_name}' (Attempt {attempt + 1}/{retries})...")
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
                return False  
            random_delay()

    return False

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

all_collected_data = []
output_path = 'common-plants1.csv'

for index, plant_name in enumerate(df['Names'], start=1):
    print(f"Processing plant {index}/{len(df['Names'])}: {plant_name}")

    if not type_prompt_in_chatgpt(plant_name): 
        print(f"Stopping script as element not found for plant '{plant_name}'.")
        break

    random_delay()

    response = extract_response()
    if response:
        all_collected_data.extend(response)

if all_collected_data:
    pd.DataFrame(all_collected_data).to_csv(output_path, index=False)
    print(f"All data saved to '{output_path}'.")
else:
    print("No data collected. Exiting.")

print("Script finished.") 



#  "Please categorize the following plant as either 'Yes' for common or 'No' if not common"
#  "A plant is considered 'common' if it is frequently grown in gardens or as an ornamental plant. "
#  "Exclude weeds, wild plants, and plants typically found in the sea (like seaweed and mangroves) 
#   from being categorized as common. "
#  "Provide the result strictly in JSON format.\n\n"