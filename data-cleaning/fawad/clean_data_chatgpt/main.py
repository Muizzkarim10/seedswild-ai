import os
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
import capsolver  # For solving CAPTCHA

# Set your CapSolver API key
capsolver.api_key = "CAP-6DC91099E6F632DB2D271DE1AA438C46"

# Function to solve CAPTCHA using CapSolver
def solve_funcaptcha_openai():
    solution = capsolver.solve({
        "type": "FunCaptchaTaskProxyLess",
        "websiteURL": "https://chat.openai.com",
        "websitePublicKey": "35536E1E-65B4-4D96-9D97-6ADB7EFF8147",
        "funcaptchaApiJSSubdomain": "https://tcr9i.chat.openai.com"
    })
    return solution

# Load the CSV file to fetch plant names
csv_file_path = "fawad.csv"
df = pd.read_csv(csv_file_path, encoding='latin1')

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='script_debug.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Start Chrome with remote debugging
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
remote_debugging_port = '9222'
user_data_dir = r'C:\Users\FAWAD\AppData\Local\Google\Chrome\User Data\Profile 2'

cmd = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port} --user-data-dir="{user_data_dir}"'
process = subprocess.Popen(cmd, shell=True)
print("Chrome launched with remote debugging.")

# Prompt user to manually log in and navigate to ChatGPT
input("Press Enter after you have navigated to the ChatGPT chat box and logged in. Make sure Chrome is still open...")

# Configure Selenium to attach to the existing Chrome session
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

# Function to add random delay
def random_delay(min_delay=3, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to type a prompt in ChatGPT's dialog box
def type_prompt_in_chatgpt(plant_name, retries=3, wait_time=10):
    prompt_text = f"Respond in only json format to my question and it could be only respone :  yes or no nothing else. Do people commonly grow the plant '{plant_name}' in their gardens or homes? yes or no?"

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
                return False
            random_delay()

    return False

# Function to extract the response
def extract_response():
    try:
        response_elements = driver.find_elements(By.CSS_SELECTOR, 'div.overflow-y-auto.p-4 code.hljs.language-json')
        if response_elements:
            response_text = response_elements[-1].text.strip()
            response_json = eval(response_text)
            return response_json.get("response", "").lower()
        return None
    except Exception as e:
        logging.error(f"Failed to extract responses: {e}")
        print(f"Failed to extract responses: {e}")
        return None

# Create or load the 'trash.csv' and 'final.csv' files
trash_path = 'trash.csv'
final_path = 'final.csv'

if os.path.exists(trash_path):
    trash_df = pd.read_csv(trash_path)
else:
    trash_df = pd.DataFrame(columns=df.columns)
    trash_df.to_csv(trash_path, index=False)

if os.path.exists(final_path):
    final_df = pd.read_csv(final_path)
else:
    final_df = pd.DataFrame(columns=df.columns)
    final_df.to_csv(final_path, index=False)

response_counter = 0

for index, row in df.iterrows():
    if row.isnull().any():
        print(f"Row {index + 1} is empty or contains NaN. Skipping.")
        continue

    plant_name = row['Seed_Name']

    print(f"Processing plant {index + 1}/{len(df)}: {plant_name}")

    if not type_prompt_in_chatgpt(plant_name):
        print(f"Stopping script as element not found for plant '{plant_name}'.")
        break

    random_delay()

    response = extract_response()

    if response:
        print(f"Response for '{plant_name}': {response}")

        if response == "yes":
            final_df = pd.concat([final_df, pd.DataFrame([row])], ignore_index=True)
            final_df.to_csv(final_path, index=False)
            print(f"Seed '{plant_name}' saved to final.csv.")
        elif response == "no":
            trash_df = pd.concat([trash_df, pd.DataFrame([row])], ignore_index=True)
            trash_df.to_csv(trash_path, index=False)
            print(f"Seed '{plant_name}' saved to trash.csv.")

        df = df.drop(index)
        df.to_csv(csv_file_path, index=False)
        print(f"Seed '{plant_name}' removed from fawad.csv.")
        response_counter += 1
    else:
        print(f"No valid response received for '{plant_name}'. Skipping.")

if df.empty:
    print("All rows processed. fawad.csv is now empty.")

print("Script finished.")

