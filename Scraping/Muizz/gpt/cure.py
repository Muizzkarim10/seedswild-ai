import subprocess
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchWindowException, WebDriverException
import pandas as pd

# List of disease names to process
disease_names = [
    "Algal Leaf Anthracnose", "Bacterial Blight", "Bacterial Spot", "Begomo_Virus",
    "Bird eye Black Spot Black_Rot", "Blast", "Blight (Early, Late)", "Brown Blight",
    "Brown Spot", "Canker", "Cedar Rust", "Cercopora", "Downy Mildew",
    "Esca (Black Measles)", "Fusarium Wilt", "Gall Midge", "Gray Light",
    "Gray Spot", "Gummy Stem Blight", "Leaf Miner", "Leaf Curl", "Leaf Mold",
    "Leaf Scars", "Leaf Scorch", "Leaf Spot", "Mosaic Virus", "Powdery Mildew",
    "Red Rot", "Rust", "Scab", "Septoria", "Sooty Mould", "Spider Mites",
    "Spotted Wilt", "Verticillium Wilt"
]

# Start Chrome with remote debugging
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
remote_debugging_port = '9222'
user_data_dir = r'C:\Users\Muizz\AppData\Local\Google\Chrome\User Data\Profile 2'

cmd = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port} --user-data-dir="{user_data_dir}"'
process = subprocess.Popen(cmd, shell=True)
print("Chrome launched with remote debugging. Please manually navigate to ChatGPT and log in if needed.")

# Prompt user to manually log in and navigate to ChatGPT
input("Press Enter after you have navigated to the ChatGPT chat box and logged in. Make sure Chrome is still open...")

# Configure Selenium to attach to the existing Chrome session
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

# Try to connect to the existing Chrome session
try:
    print("Attempting to connect to Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome. Current page title:", driver.title)
except WebDriverException as e:
    logging.error(f"Failed to connect to Chrome: {e}")
    print(f"Failed to connect to Chrome: {e}")
    exit()

# Function to add a random delay to mimic human interaction
def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to type a prompt in ChatGPT's dialog box
def type_prompt_in_chatgpt(disease_name, retries=3, wait_time=10):
    prompt_text = (
        f"Provide detailed data in the following format for the disease '{disease_name}':\n"
        "{{\n"
        "  'Disease': '{disease_name}',\n"
        "  'Identification': 'Provide detailed identification information specific to {disease_name}',\n"
        "  'Solution': 'Include specific solutions and cultural practices to manage {disease_name}',\n"
        "  'Additional Tips': 'Offer additional tips for effectively managing {disease_name}'\n"
        "}}\n"
        "Only provide information as per this format, with no additional text."
    )

    for attempt in range(retries):
        try:
            # Check if the Chrome window is still active
            driver.current_window_handle
            print(f"Attempting to send prompt for '{disease_name}' (Attempt {attempt + 1}/{retries})...")

            # Wait for the input box to be visible and clickable
            input_box = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "prompt-textarea"))  # Updated selector for contenteditable div
            )
            input_box.click()

            # Clear any existing text and enter the new prompt
            driver.execute_script("arguments[0].innerText = '';", input_box)  # Clear text if any
            input_box.send_keys(prompt_text)  # Send keys to the div

            random_delay()
            input_box.send_keys(Keys.RETURN)  # Press Enter to submit
            print(f"Prompt sent for '{disease_name}'.")
            return True
        except (NoSuchWindowException, StaleElementReferenceException, TimeoutException) as e:
            logging.error(f"Error sending prompt for '{disease_name}': {e}")
            print(f"Error sending prompt for '{disease_name}': {e}")
            if attempt == retries - 1:
                print(f"Failed to send prompt for '{disease_name}' after {retries} attempts.")
                return False
            random_delay()

    return False

# Function to extract the response
def extract_response():
    try:
        response_elements = driver.find_elements(By.CSS_SELECTOR, 'div.overflow-y-auto.p-4 code.hljs.language-json')
        responses = []

        for response_element in response_elements:
            response_text = response_element.text
            try:
                disease_data = json.loads(response_text)
                responses.append(disease_data)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON received: {response_text}")
                print(f"Invalid JSON received, skipping.")

        return responses

    except Exception as e:
        logging.error(f"Failed to extract responses: {e}")
        print(f"Failed to extract responses: {e}")
        return []

# Main processing loop to collect data
all_collected_data = []
output_path = 'disease_cure_output.csv'  # Specify output file

for index, disease_name in enumerate(disease_names, start=1):
    print(f"Processing disease {index}/{len(disease_names)}: {disease_name}")

    # Attempt to type the prompt
    if not type_prompt_in_chatgpt(disease_name):  # If sending the prompt fails
        print(f"Stopping script as element not found for disease '{disease_name}'.")
        break  # Exit the loop if element cannot be interacted with

    random_delay()

    # Attempt to extract response
    response = extract_response()
    if response:
        all_collected_data.extend(response)

# Save all collected data at the end
if all_collected_data:
    pd.DataFrame(all_collected_data).to_csv(output_path, index=False)
    print(f"All data saved to '{output_path}'.")
else:
    print("No data collected. Exiting.")

print("Script finished.")
