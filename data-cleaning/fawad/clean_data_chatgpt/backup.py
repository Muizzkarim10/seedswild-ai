# import os
# import subprocess
# import time
# import random
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import logging
# from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
# import capsolver  # For solving CAPTCHA

# # Set your CapSolver API key
# capsolver.api_key = "CAP-6DC91099E6F632DB2D271DE1AA438C46"

# # Function to solve CAPTCHA using CapSolver
# def solve_funcaptcha_openai():
#     solution = capsolver.solve({
#        "type": "FunCaptchaTaskProxyLess",
#         "websiteURL": "https://chat.openai.com",
#         "websitePublicKey": "35536E1E-65B4-4D96-9D97-6ADB7EFF8147",
#         "funcaptchaApiJSSubdomain": "https://tcr9i.chat.openai.com"
#     })
#     return solution

# # Load the CSV file to fetch plant names
# csv_file_path = "fawad.csv"  # Update to absolute path if needed
# df = pd.read_csv(csv_file_path, encoding='latin1')  # or 'ISO-8859-1', or 'utf-16'

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, filename='script_debug.log', filemode='w',
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# # Start Chrome with remote debugging
# chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# remote_debugging_port = '9222'      
# user_data_dir = r'C:\Users\FAWAD\AppData\Local\Google\Chrome\User Data\Profile 4'
    

# cmd = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port} --user-data-dir="{user_data_dir}"'
# process = subprocess.Popen(cmd, shell=True)
# print("Chrome launched with remote debugging.")

# # Prompt user to manually log in and navigate to ChatGPT
# input("Press Enter after you have navigated to the ChatGPT chat box and logged in. Make sure Chrome is still open...")

# # Configure Selenium to attach to the existing Chrome session
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

# # Try to connect to the existing Chrome session
# try:
#     print("Attempting to connect to Chrome...")
#     driver = webdriver.Chrome(options=chrome_options)
#     print("Connected to Chrome. Current page title: " + driver.title)
# except Exception as e:
#     logging.error(f"Failed to connect to Chrome: {e}")
#     print(f"Failed to connect to Chrome: {e}")
#     exit()

# # Function to wait for CAPTCHA resolution using CapSolver
# def wait_for_captcha(timeout=300):
#     print("Captcha detected. Attempting to solve using CapSolver...")
#     start_time = time.time()

#     while time.time() - start_time < timeout:
#         try:
#             solution = solve_funcaptcha_openai()
#             token = solution["token"]
#             print(f"Captcha solved. Token: {token}")
#             return True
#         except Exception as e:
#             print(f"Failed to solve CAPTCHA: {e}")
#             time.sleep(5)

#     print("Failed to solve CAPTCHA within the timeout. Exiting script.")
#     driver.quit()
#     exit()

# # Function to add random delay
# def random_delay(min_delay=3, max_delay=5):
#     time.sleep(random.uniform(min_delay, max_delay))

# # Function to type a prompt in ChatGPT's dialog box
# def type_prompt_in_chatgpt(plant_name, retries=3, wait_time=10):
#     prompt_text = f"Only in JSON format ..yes or no.... no explanations  [response : yes/no ] in json format. Do people commonly grow the plant '{plant_name}' in their gardens or homes?"

#     for attempt in range(retries):
#         try:
#             print(f"Attempting to send prompt for '{plant_name}' (Attempt {attempt + 1}/{retries})...")
#             input_box = WebDriverWait(driver, wait_time).until(
#                 EC.visibility_of_element_located((By.ID, 'prompt-textarea'))
#             )
#             input_box.click()
#             input_box.clear()
#             input_box.send_keys(prompt_text)
#             random_delay()
#             input_box.send_keys(Keys.RETURN)
#             print(f"Prompt sent for '{plant_name}'.")
#             return True
#         except (StaleElementReferenceException, TimeoutException) as e:
#             logging.error(f"Error sending prompt for '{plant_name}': {e}")
#             print(f"Error sending prompt for '{plant_name}': {e}")
#             wait_for_captcha()
#             if attempt == retries - 1:
#                 print(f"Failed to send prompt for '{plant_name}' after {retries} attempts. Stopping.")
#                 return False
#             random_delay()

#     return False

# # Function to extract the response
# def extract_response():
#     try:
#         response_elements = driver.find_elements(By.CSS_SELECTOR, 'div.overflow-y-auto.p-4 code.hljs.language-json')
#         if response_elements:
#             response_text = response_elements[-1].text.strip()
#             response_json = eval(response_text)
#             return response_json.get("response", "").lower()
#         return None
#     except Exception as e:
#         logging.error(f"Failed to extract responses: {e}")
#         print(f"Failed to extract responses: {e}")
#         return None

# # Create or open the CSV files to store filtered data
# output_path = 'final.csv'
# trash_path = 'trash.csv'

# try:
#     final_df = pd.read_csv(output_path)
#     trash_df = pd.read_csv(trash_path)
# except FileNotFoundError:
#     final_df = pd.DataFrame(columns=df.columns)
#     trash_df = pd.DataFrame(columns=df.columns)

# response_counter = 0

# # Process each plant name
# for index, row in df.iterrows():
#     if row.isnull().any():
#         print(f"Row {index + 1} is empty or contains NaN. Skipping.")
#         continue

#     plant_name = row['Seed_Name']

#     print(f"Processing plant {index + 1}/{len(df)}: {plant_name}")

#     if response_counter > 0 and response_counter % 10 == 0:
#         print("Refreshing the page...")
#         driver.refresh()
#         random_delay(10, 15)

#     if not type_prompt_in_chatgpt(plant_name):
#         print(f"Stopping script as element not found for plant '{plant_name}'.")
#         break

#     random_delay()

#     response = extract_response()





















# import os
# import subprocess
# import time
# import random
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import logging
# from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
# import capsolver  # For solving CAPTCHA

# # Set your CapSolver API key
# capsolver.api_key = "CAP-6DC91099E6F632DB2D271DE1AA438C46"

# # Function to solve CAPTCHA using CapSolver
# def solve_funcaptcha_openai():
#     solution = capsolver.solve({
#         "type": "FunCaptchaTaskProxyLess",
#         "websiteURL": "https://chat.openai.com",
#         "websitePublicKey": "35536E1E-65B4-4D96-9D97-6ADB7EFF8147",
#         "funcaptchaApiJSSubdomain": "https://tcr9i.chat.openai.com"
#     })
#     return solution

# # Load the CSV file to fetch plant names
# csv_file_path = "fawad.csv"  # Update to absolute path if needed
# df = pd.read_csv(csv_file_path, encoding='latin1')  # or 'ISO-8859-1', or 'utf-16'

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, filename='script_debug.log', filemode='w',
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# # Start Chrome with remote debugging
# chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# remote_debugging_port = '9222'      
# user_data_dir = r'C:\Users\FAWAD\AppData\Local\Google\Chrome\User Data\Profile 4'

# cmd = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port} --user-data-dir="{user_data_dir}"'
# process = subprocess.Popen(cmd, shell=True)
# print("Chrome launched with remote debugging.")

# # Prompt user to manually log in and navigate to ChatGPT
# input("Press Enter after you have navigated to the ChatGPT chat box and logged in. Make sure Chrome is still open...")

# # Configure Selenium to attach to the existing Chrome session
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

# # Try to connect to the existing Chrome session
# try:
#     print("Attempting to connect to Chrome...")
#     driver = webdriver.Chrome(options=chrome_options)
#     print("Connected to Chrome. Current page title: " + driver.title)
# except Exception as e:
#     logging.error(f"Failed to connect to Chrome: {e}")
#     print(f"Failed to connect to Chrome: {e}")
#     exit()

# # Checkpoint file to track processed seeds
# checkpoint_file = "processed_plants.txt"

# # Load processed seeds from the checkpoint file
# if os.path.exists(checkpoint_file):
#     with open(checkpoint_file, "r") as file:
#         processed_seeds = set(line.strip() for line in file)
# else:
#     processed_seeds = set()

# # Function to update the checkpoint file
# def update_checkpoint(plant_name):
#     with open(checkpoint_file, "a") as file:
#         file.write(f"{plant_name}\n")

# # Function to wait for CAPTCHA resolution using CapSolver
# def wait_for_captcha(timeout=300):
#     print("Captcha detected. Attempting to solve using CapSolver...")
#     start_time = time.time()

#     while time.time() - start_time < timeout:
#         try:
#             solution = solve_funcaptcha_openai()
#             token = solution["token"]
#             print(f"Captcha solved. Token: {token}")
#             return True
#         except Exception as e:
#             print(f"Failed to solve CAPTCHA: {e}")
#             time.sleep(5)

#     print("Failed to solve CAPTCHA within the timeout. Exiting script.")
#     driver.quit()
#     exit()

# # Function to add random delay
# def random_delay(min_delay=3, max_delay=5):
#     time.sleep(random.uniform(min_delay, max_delay))

# # Function to type a prompt in ChatGPT's dialog box
# def type_prompt_in_chatgpt(plant_name, retries=3, wait_time=10):
#     prompt_text = f"I'm ordering you to response in json format ..yes or no....Do people commonly grow the plant '{plant_name}' in their gardens or homes?"

#     for attempt in range(retries):
#         try:
#             print(f"Attempting to send prompt for '{plant_name}' (Attempt {attempt + 1}/{retries})...")
#             input_box = WebDriverWait(driver, wait_time).until(
#                 EC.visibility_of_element_located((By.ID, 'prompt-textarea'))
#             )
#             input_box.click()
#             input_box.clear()
#             input_box.send_keys(prompt_text)
#             random_delay()
#             input_box.send_keys(Keys.RETURN)
#             print(f"Prompt sent for '{plant_name}'.")
#             return True
#         except (StaleElementReferenceException, TimeoutException) as e:
#             logging.error(f"Error sending prompt for '{plant_name}': {e}")
#             print(f"Error sending prompt for '{plant_name}': {e}")
#             wait_for_captcha()
#             if attempt == retries - 1:
#                 print(f"Failed to send prompt for '{plant_name}' after {retries} attempts. Stopping.")
#                 return False
#             random_delay()

#     return False

# # Function to extract the response
# def extract_response():
#     try:
#         response_elements = driver.find_elements(By.CSS_SELECTOR, 'div.overflow-y-auto.p-4 code.hljs.language-json')
#         if response_elements:
#             response_text = response_elements[-1].text.strip()
#             response_json = eval(response_text)
#             return response_json.get("response", "").lower()
#         return None
#     except Exception as e:
#         logging.error(f"Failed to extract responses: {e}")
#         print(f"Failed to extract responses: {e}")
#         return None

# # Create or open the CSV files to store filtered data
# final_output_path = 'final.csv'
# trash_output_path = 'trash.csv'

# # Create empty files or load existing data
# def append_to_csv(output_path, row):
#     try:
#         existing_df = pd.read_csv(output_path)
#         existing_df = existing_df.append(row, ignore_index=True)
#         existing_df.to_csv(output_path, index=False)
#     except FileNotFoundError:
#         pd.DataFrame([row]).to_csv(output_path, index=False)

# response_counter = 0

# # Filtered rows to keep track of the plants that will be saved
# for index, row in df.iterrows():
#     if row.isnull().any():
#         print(f"Row {index + 1} is empty or contains NaN. Skipping.")
#         continue

#     plant_name = row['Seed_Name']

#     if plant_name in processed_seeds:
#         print(f"Seed '{plant_name}' is already processed. Skipping.")
#         continue

#     print(f"Processing plant {index + 1}/{len(df)}: {plant_name}")

#     if response_counter > 0 and response_counter % 10 == 0:
#         print("Refreshing the page...")
#         driver.refresh()
#         random_delay(10, 15)

#     if not type_prompt_in_chatgpt(plant_name):
#         print(f"Stopping script as element not found for plant '{plant_name}'.")
#         break

#     random_delay()

#     response = extract_response()

#     if response:
#         print(f"Response for '{plant_name}': {response}")

#         if response == "yes":
#             append_to_csv(final_output_path, row.to_dict())
#             print(f"Seed '{plant_name}' saved to final.csv.")
#         elif response == "no":
#             append_to_csv(trash_output_path, row.to_dict())
#             print(f"Seed '{plant_name}' saved to trash.csv.")
        
#         processed_seeds.add(plant_name)
#         update_checkpoint(plant_name)
#         response_counter += 1
#     else:
#         print(f"No valid response received for '{plant_name}'. Skipping.")

#     # Remove processed seed from the original `fawad.csv`
#     df = df[df['Seed_Name'] != plant_name]
#     df.to_csv(csv_file_path, index=False)

#     if response_counter > 0 and response_counter % 5 == 0:
#         print("Saving checkpoint...")
#         processed_seeds = set(row.strip() for row in open(checkpoint_file).readlines())

# print("Script finished.")

















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
user_data_dir = r'C:\Users\FAWAD\AppData\Local\Google\Chrome\User Data\Profile 4'

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

# Checkpoint file to track processed seeds
checkpoint_file = "processed_plants.txt"

if os.path.exists(checkpoint_file):
    with open(checkpoint_file, "r") as file:
        processed_seeds = set(line.strip() for line in file)
else:
    processed_seeds = set()

# Function to update the checkpoint file
def update_checkpoint(plant_name):
    with open(checkpoint_file, "a") as file:
        file.write(f"{plant_name}\n")

# Function to add random delay
def random_delay(min_delay=3, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to type a prompt in ChatGPT's dialog box
def type_prompt_in_chatgpt(plant_name, retries=3, wait_time=10):
    prompt_text = f"I'm ordering you to respond in JSON format. Yes or No: Do people commonly grow the plant '{plant_name}' in their gardens or homes?"

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

    if plant_name in processed_seeds:
        print(f"Seed '{plant_name}' is already processed. Skipping.")
        continue

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
        processed_seeds.add(plant_name)
        update_checkpoint(plant_name)
        response_counter += 1
    else:
        print(f"No valid response received for '{plant_name}'. Skipping.")

if df.empty:
    print("All rows processed. fawad.csv is now empty.")

print("Script finished.")
