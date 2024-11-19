import pandas as pd
from playwright.sync_api import sync_playwright
import logging

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

link = "https://territorialseed.com/collections/flower-plants"
names = []
image_url = []
Description = []

def save_to_csv():
    global names, Description, image_url

    max_length = max(len(names), len(Description), len(image_url))

    def pad_list(lst, length):
        return lst + [None] * (length - len(lst))

    names = pad_list(names, max_length)
    image_url = pad_list(image_url, max_length)
    Description = pad_list(Description, max_length)

    df = pd.DataFrame({
        'Name': names,
        'Image_URL': image_url,
        'Description': Description
    })

    df.to_csv('sheet3.csv', index=False)
    logging.info('Data saved to CSV file.')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(link)

    # Scroll down until the end of the page initially
    previous_height = None
    while True:
        # Scroll by evaluating JavaScript
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")

        # Wait a moment for new content to load
        page.wait_for_timeout(1000)

        # Get the new height after scrolling
        current_height = page.evaluate('document.body.scrollHeight')
        
        # If the height hasn't changed, we are at the end of the page
        if previous_height == current_height:
            break
        previous_height = current_height

    logging.info("Reached the end of the page")

    # Ensure the product list is visible before interacting
    page.wait_for_selector('div.products--list', timeout=5000)

    # Locate all individual product items using the correct selector
    li_elements = page.locator('div.products--box')
    product_count = li_elements.count()

    logging.info(f"Total products found: {product_count}")
    print(f"Total products found: {product_count}")

    for i in range(product_count):
        logging.info(f"Processing product {i + 1} out of {product_count}")

        try:
            # Get the correct product element and click it
            li_elements.nth(i).click()

            # Wait for the product page to load
            page.wait_for_selector("h1.product__title.show-desktop", timeout=10000)

            # Fetch product name, ensuring to pick the first match
            h1_tag = page.locator("h1.product__title.show-desktop").first
            names.append(h1_tag.text_content().strip() or "N/A")
            logging.info(f"Retrieved name: {names[-1]}")

            # Fetch product description
            text = page.locator("div.html--contents").first
            Description.append(text.text_content().strip() or "N/A")
            logging.info(f"Retrieved description: {Description[-1]}")

            # Fetch first image URL, handling potential lazy-loading (e.g., data-src attribute)
            img1 = page.locator("div.slick-slide.slick-current.slick-active img").first
            src1 = img1.get_attribute('src') or img1.get_attribute('data-src') or "N/A"
            image_url.append(src1)
            logging.info(f"Retrieved image URL: {src1}")

        except Exception as e:
            logging.error(f"Error processing product {i + 1}: {e}")

        finally:
            try:
                # Go back to the product list and wait for it to load again
                page.go_back(timeout=15000)
                page.wait_for_selector('div.products--list', timeout=10000)
                logging.info(f"Navigated back to the product list after processing product {i + 1}")

                # Scroll down to the end of the page after returning to the list
                previous_height = None
                while True:
                    # Scroll by evaluating JavaScript
                    page.evaluate("window.scrollBy(0, document.body.scrollHeight)")

                    # Wait a moment for new content to load
                    page.wait_for_timeout(1000)

                    # Get the new height after scrolling
                    current_height = page.evaluate('document.body.scrollHeight')
                    
                    # If the height hasn't changed, we are at the end of the page
                    if previous_height == current_height:
                        break
                    previous_height = current_height

                logging.info("Reached the end of the page after navigating back")

            except Exception as e:
                logging.error(f"Error navigating back after product {i + 1}: {e}")
                break  # Exit loop if go_back fails

    save_to_csv()
    browser.close()
    logging.info('Browser closed.')
