import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from playwright_stealth import stealth_sync


link = "https://davesgarden.com/products/ps/c/759/0"
names = []
image_URL1 = []
image_URL2 = []
image_URL3 = []
Description = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    stealth_sync(page)
    page.goto(link)
    # page.wait_for_selector("input[type='checkbox']")
    # page.click("input[type='checkbox']")
    # page.wait_for_selector("table")
    # page.wait_for_selector("table")
        
        # Extract all rows from the table
    rows = page.query_selector_all("table tr")
        
        # Iterate over each row
    for row in rows:
            # Extract all columns/cells in the current row
       cells = row.query_selector_all("td")
            # Print or process the text content of each cell
       row_data = [cell.text_content().strip() for cell in cells]
       print(row_data)
        
#         # Wait for the div to be present and visible before clicking
#         try:
#             page.wait_for_selector(div_selector, timeout=15000)  # 15-second timeout
#             page.click(div_selector)
#             page.wait_for_timeout(10000)  # Wait for page to load after click
#         except Exception as e:
#             print(f"Error clicking div with data-index={i}: {e}")
#             continue
        
#         html = page.inner_html('.product-details-full-content-header')
#         soup = BeautifulSoup(html, 'html.parser')
        
#         h1_tag = soup.select_one('.brand-h2.product-name h1')
#         if h1_tag:
#             text = h1_tag.get_text(strip=True)
#             names.append(text)
#         else:
#             print("No <h1> tag found.")
#             names.append("No name found")
        
#         # Wait for the images to be visible and then get their src attributes
#         image_selector = 'img.d-block.img-fluid'
#         try:
#             page.wait_for_selector(image_selector, timeout=10000)  # Wait for images to load
#             images = page.locator(image_selector).element_handles()  # Get all matching images
#             if len(images) >= 3:  # Check if there are at least 3 images
#                 src1 = images[0].get_attribute('src')
#                 src2 = images[1].get_attribute('src')
#                 src3 = images[2].get_attribute('src')
                
#                 if src1:
#                     image_URL1.append(src1)
#                 else:
#                     image_URL1.append("No src found for image 1")
                
#                 if src2:
#                     image_URL2.append(src2)
#                 else:
#                     image_URL2.append("No src found for image 2")
                
#                 if src3:
#                     image_URL3.append(src3)
#                 else:
#                     image_URL3.append("No src found for image 3")
#             else:
#                 print(f"Less than 3 images found for item {i}")
#                 image_URL1.append("Not enough images")
#                 image_URL2.append("Not enough images")
#                 image_URL3.append("Not enough images")
        
#         except Exception as e:
#             print(f"Error retrieving image src: {e}")
#             image_URL1.append("Error")
#             image_URL2.append("Error")
#             image_URL3.append("Error")
        
#         p_tag = page.query_selector('#collapsible-details-1')
#         if p_tag:
#             p_text = p_tag.text_content()
#             Description.append(p_text)
#         else:
#             print("Can't find description.")
#             Description.append("No description found")
        
#         page.go_back()

# # Create a DataFrame with three image URL columns
# df = pd.DataFrame({
#     'Names': names,
#     'Description': Description,
#     'Image_URL1': image_URL1,
#     'Image_URL2': image_URL2,
#     'Image_URL3': image_URL3
# })
# df.to_csv('sheet1.csv', index=False)
