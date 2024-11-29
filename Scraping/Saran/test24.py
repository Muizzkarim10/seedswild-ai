import pandas as pd
from playwright.sync_api import sync_playwright
import logging

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

link = "https://www.kingsseeds.com/products/vegetable-seeds"
names = []
image_URL1 = []
descriptions = []

def save_to_csv():
    global names, image_URL1, descriptions

    max_length = max(len(names), len(image_URL1), len(descriptions))

    def pad_list(lst, length):
        return lst + [None] * (length - len(lst))

    names = pad_list(names, max_length)
    image_URL1 = pad_list(image_URL1, max_length)
    descriptions = pad_list(descriptions, max_length)

    df = pd.DataFrame({
        'Name': names,
        'Image URL 1': image_URL1,
        'Description': descriptions
    })

    df.to_csv('sheet1.csv', index=False)
    logging.info('Data saved to CSV file.')

def scrape_data(page):
    product_elements = page.locator('div.row')
    products = product_elements.locator('div.col-xl-2.col-md-4.col-sm-3.col-xs-12.block')
    
    count = products.count()
    links = []

    for i in range(count):
        a = products.nth(i).locator("a")  # Locate the <a> tag
        href = a.get_attribute("href")  # Extract the href attribute
        links.append(href)  # Append the href to the links

    for product_link in links:
        page.goto(product_link)
        page.wait_for_load_state('networkidle', timeout=15000)  # Wait for the page to load    

        try:
            h1_tag = page.locator("//h1[@class='prodDetailsName']")
            names.append(h1_tag.text_content().strip() or "N/A")
            logging.info(f"Retrieved name: {names[-1]}")
        except Exception as e:
            logging.error(f"Error retrieving <h1> tag: {e}")
            names.append("N/A")

        try:
            img1 = page.locator("//img[contains(@src, '/PRODUCT_IMAGES/')]")
            src1 = img1.get_attribute('src') or "N/A"
            image_URL1.append(src1)
            logging.info(f"Retrieved image URL 1: {src1}")
        except Exception as e:
            logging.error(f"Error retrieving image: {e}")
            image_URL1.append("N/A")

        try:
            description = page.locator("//div[@class='__prod-sub-desc']/p").text_content() or "N/A"
            descriptions.append(description)
            logging.info(f"Retrieved description: {description}")
        except Exception as e:
            logging.error(f"Error retrieving description: {e}")
            descriptions.append("N/A")

        page.go_back()
        page.wait_for_timeout(3000)  # Wait for a bit before going back

    try:
        next_button = page.locator("//a[@id='lnkNext2']")
        if next_button.is_visible():
            next_button.click()
            page.wait_for_load_state('networkidle', timeout=10000)
    except Exception as e:
        logging.error(f"Error clicking 'Next' button: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    try:
        page.goto(link)
        page.wait_for_timeout(5000)  # Increased timeout for loading
        scrape_data(page)
    except Exception as e:
        logging.error(f"Failed to navigate to {link}: {e}")

    save_to_csv()
    browser.close()
    logging.info('Browser closed.')