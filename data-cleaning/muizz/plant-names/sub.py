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
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

csv_file_path = "sample.csv"  
df = pd.read_csv(csv_file_path, encoding='latin1') 

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

def type_prompt_in_chatgpt(plant_name, retries=3, wait_time=5):
    prompt_text = (
    "Is the plant common or not? A plant is considered 'common' if it is frequently grown in gardens "
    "or as an ornamental plant. Exclude weeds, wild plants, and plants typically found in the sea "
    "(like seaweed and mangroves) from being categorized as common. "
    "Respond only in this JSON format: {{'response': 'Yes' or 'No'}}."
    f"Plant name : '{plant_name}'"
)
    for attempt in range(retries):
        try:
            print(f"Attempting to send prompt for '{plant_name}' (Attempt {attempt + 1}/{retries})...")
            input_box = WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located((By.ID, 'prompt-textarea'))
            )
            input_box.click()
            input_box.clear() 
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
        response_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.overflow-y-auto.p-4 code.hljs.language-json')) 
        )
        response_text = response_element.text.strip()
        print(f"Extracted raw response: {response_text}")
        
        try:
            response_dict = eval(response_text) 
            return response_dict.get("response", "").lower()
        except (SyntaxError, NameError):
            print("Failed to parse response as dictionary. Raw text:", response_text)
            return None
    except TimeoutException:
        print("No response element found within the timeout period.")
        return None
    except Exception as e:
        logging.error(f"Failed to extract responses: {e}")
        print(f"Failed to extract responses: {e}")
        return None


output_path = 'temp.csv'
filtered_rows = []

try:
    existing_df = pd.read_csv(output_path)
except FileNotFoundError:
    existing_df = pd.DataFrame(columns=df.columns)

for index, row in df.iterrows():
    plant_name = row['Names']
    print(f"Processing plant {index + 1}/{len(df)}: {plant_name}")

    if not type_prompt_in_chatgpt(plant_name):
        print(f"Stopping script as element not found for plant '{plant_name}'.")
        break

    random_delay()

    response = extract_response()
    if response:
        print(f"Response for '{plant_name}': {response}")
        if response == "yes": 
            filtered_rows.append(row) 
            print(f"Seed '{plant_name}' saved.")
        elif response == "no":
            print(f"Seed '{plant_name}' was not saved because response was 'No'.")
    else:
        print(f"No valid response received for '{plant_name}'. Skipping.")

    if filtered_rows:
        filtered_df = pd.DataFrame(filtered_rows, columns=df.columns)  
        filtered_df.to_csv(output_path, mode='w', index=False)
        print(f"Data saved to '{output_path}' after processing '{plant_name}'.")

if not filtered_rows:
    print("No rows matched the criteria. Exiting.")

print("Script finished.")


#  "Respond only in this  json format: {{'response': 'Yes' or 'No'}}."
#  "i am provinding a sinle plant name in a single prompt dont divide that name into two."
#  "A plant is considered 'common' if it is frequently grown in gardens or as an ornamental plant. "
#  "Exclude weeds, wild plants, and plants typically found in the sea (like seaweed and mangroves) 
#   from being categorized as common. "