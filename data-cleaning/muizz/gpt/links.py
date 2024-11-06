import subprocess
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging

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

# Prompt user to manually log in
input("Press Enter after you have navigated to the listings page and logged in. Make sure Chrome is still open...")

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