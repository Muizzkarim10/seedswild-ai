import pandas as pd
from playwright.sync_api import sync_playwright
import logging

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

base_url = "https://agrohaitai.com"
link = f"{base_url}/collections/all?page=13"
names = []
image_URL1 = []
image_URL2 = []
Description = []
Other_Name = []

def save_to_csv():
    global names, image_URL1, Description, Other_Name, image_URL2

    max_length = max(len(names), len(image_URL1), len(Description), len(Other_Name), len(image_URL2))

    def pad_list(lst, length):
        return lst + [None] * (length - len(lst))

    names = pad_list(names, max_length)
    image_URL1 = pad_list(image_URL1, max_length)
    Description = pad_list(Description, max_length)
    Other_Name = pad_list(Other_Name, max_length)
    image_URL2 = pad_list(image_URL2, max_length)

    df = pd.DataFrame({
        'Name': names,
        'Other_Name': Other_Name,
        'Image URL 1': image_URL1,
        'Image URL 2': image_URL2,
        'Description': Description,
    })

    df.to_csv('sheet13.csv', index=False)
    logging.info('Data saved to CSV file.')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(link)
    
    # Locate the parent div and extract all href links to the product pages
    div_locator = page.locator('div.product-list.product-list--collection.product-list--with-sidebar')
    product_links = div_locator.locator('a.product-item__image-wrapper').all()  # Get all anchor elements with href within the div

    # Extract the href attribute for each anchor tag and prepend the base URL
    product_urls = [base_url + link.get_attribute('href') for link in product_links]

    # Iterate over each product URL
    for product_url in product_urls:
        try:
            page.goto(product_url)
            try:
                h4_tag = page.locator('//*[@id="shopify-section-product-template"]/section/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/h4')
                names.append(h4_tag.text_content() or "N/A")
                logging.info(f"Retrieved name: {names[-1]}")
            except Exception as e:
                logging.error(f"Error retrieving <h4> tag: {e}")
                names.append("N/A")
            
            try:
                h1_tag = page.locator('//*[@id="shopify-section-product-template"]/section/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/h1')
                Other_Name.append(h1_tag.text_content() or "N/A")
                logging.info(f"Retrieved other name: {Other_Name[-1]}")
            except Exception as e:
                logging.error(f"Error retrieving <h1> tag: {e}")
                Other_Name.append("N/A")
            
            try:
                img1 = page.locator('//*[@id="shopify-section-product-template"]/section/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div/img')
                src1 = img1.get_attribute('src') or "N/A"
                image_URL1.append(src1)
                logging.info(f"Retrieved image URL 1: {src1}")
            except Exception as e:
                logging.error(f"Error retrieving img1: {e}")
                image_URL1.append("N/A")
            
            try:
                page.click('//*[@id="shopify-section-product-template"]/section/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div/a[2]/div')
                try:
                    img2 = page.locator('//*[@id="shopify-section-product-template"]/section/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/img')
                    src2 = img2.get_attribute('src') or "N/A"
                    image_URL2.append(src2)
                    logging.info(f"Retrieved image URL 2: {src2}")
                except Exception as e:
                    logging.error(f"Error retrieving img2: {e}")
                    image_URL2.append("N/A")
            except:
                logging.error(f"No second image available")
                image_URL2.append("N/A")
            
            try:
                text = page.locator('//*[@id="shopify-section-product-template"]/section/div[1]/div[2]/div/div[3]/div/div[2]')
                Description.append(text.text_content() or "N/A")
                logging.info(f"Retrieved description: {Description[-1]}")
            except Exception as e:
                logging.error(f"Error retrieving description: {e}")
                Description.append("N/A")
        
        except Exception as e:
            logging.error(f"Error processing product URL {product_url}: {e}")
    
    save_to_csv()
    browser.close()
    logging.info('Browser closed.')
