import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

link = "https://shop.seedsavers.org/flower/flowers"
names = []
image_URL = []
Description = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto(link)
    
    for i in range(1, 3):
        # Corrected the selector to target the 'li' element with the attribute 'data-track-productlist-position'
        li_selector = f'li[data-track-productlist-position="{i}"]'
        page.click(li_selector)
        page.wait_for_timeout(10000)
        
        html = page.inner_html('.product-details-full-content-header')
        soup = BeautifulSoup(html, 'html.parser')
        
        h1_tag = soup.select_one('.product-details-full-content-header-title h1')
        if h1_tag:
            text = h1_tag.get_text(strip=True)
            names.append(text)
        else:
            print("No <h1> tag found.")
        
        # Wait for the image to be visible and then get its src attribute
        image_selector = 'img.center-block'
        try:
            page.wait_for_selector(image_selector, timeout=10000)  # Adjust the timeout as needed
            src = page.locator(image_selector).get_attribute('src')
            if src:
                image_URL.append(src)
            else:
                print("No src attribute found.")
        except Exception as e:
            print(f"Error retrieving image src: {e}")
        
        p_tag = page.locator('.product-details-information-tab-content-container p')
        p_text = p_tag.text_content()
        if p_text:
            Description.append(p_text)
        else:
            print("Can't find description.")
        
        page.go_back()

print(names)
print(Description)
print(image_URL)



# df = pd.DataFrame({
#     'Names': names,
#     'Description': Description,
#     'Image_URL': image_URL
# })
# df.to_csv('sheet1.csv', index=False)

    