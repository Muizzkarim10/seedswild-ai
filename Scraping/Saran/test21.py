import pandas as pd
from playwright.sync_api import sync_playwright
import logging

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

link = "https://eliseseeds.com/products/?v=ebakhjd3i1&l=abd0c9543821f67e"
names = []
image_URL1 = []
Details = []

def save_to_csv():
    global names, image_URL1, Details

    max_length = max(len(names), len(image_URL1), len(Details))

    def pad_list(lst, length):
        return lst + [None] * (length - len(lst))

    names = pad_list(names, max_length)
    image_URL1 = pad_list(image_URL1, max_length)
    Details = pad_list(Details, max_length)

    df = pd.DataFrame({
        'Name': names,
        'Image URL 1': image_URL1,
        'Details': Details,
    })

    df.to_csv('sheet2.csv', index=False)
    logging.info('Data saved to CSV file.')

def scrape_data(page):
    product_elements = page.locator('//div[@class="row"]/div[@class="col-sm-12 col-md-6 col-lg-4 mb-2"]')

    for i in range(product_elements.count()):
        product = product_elements.nth(i)
        try:
            # Click on the product to go to the list
            product.locator('.blog-card__image a').click()
            page.wait_for_timeout(2000)  # Wait for the page to load

            # Check if inner products are available
            if page.locator('//div[@class="row"]/div[@class="col-sm-12 col-md-6 col-lg-4 mb-2"]').count() > 0:
                inner_product_elements = page.locator('//div[@class="row"]/div[@class="col-sm-12 col-md-6 col-lg-4 mb-2"]')
                for j in range(inner_product_elements.count()):
                    inner_product = inner_product_elements.nth(j)
                    inner_product.locator('.blog-card__image a').click()  # Click to get to the detail page
                    page.wait_for_timeout(2000)  # Wait for the page to load
                    
                    try:
                        h1_tag = page.locator("//div[@class='product_detail_review_box mt-0']/h2")
                        names.append(h1_tag.text_content().strip() or "N/A")
                        logging.info(f"Retrieved name: {names[-1]}")
                    except Exception as e:
                        logging.error(f"Error retrieving <h2> tag: {e}")
                        names.append("N/A")
        
                    try:
                        img1 = page.locator("//div[@class='col-sm-6 mb-2']/img")
                        src1 = img1.get_attribute('src') or "N/A"
                        image_URL1.append(src1)
                        logging.info(f"Retrieved image URL 1: {src1}")
                    except Exception as e:
                        logging.error(f"Error retrieving img1: {e}")
                        image_URL1.append("N/A")

                    try:
                        details = page.locator("//div[@class='product_detail_text product-details']/div/ul")
                        Details.append(details.text_content().strip() or "N/A")
                        logging.info(f"Retrieved details: {Details[-1]}")
                    except Exception as e:
                        logging.error(f"Error retrieving details: {e}")
                        Details.append("N/A")

                    page.go_back()  # Go back to the list after collecting data
                    page.wait_for_timeout(1000)  # Adjusted wait time

            page.go_back()  # Go back to the outer list after finishing the inner list
            page.wait_for_timeout(2000)  # Adjusted wait time

        except Exception as e:
            logging.error(f"Error interacting with product: {e}")
            page.go_back()
            page.wait_for_timeout(2000)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(link)
    page.wait_for_timeout(5000)  # Wait for the main page to load
    scrape_data(page)
    save_to_csv()
    browser.close()
    logging.info('Browser closed.')
