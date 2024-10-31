import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

link = "https://americanseedco.com/"
lists = []
list2 = []
names = []
image_URL = []
Description = []

def scrape_data(page):
    html = page.inner_html('#content')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract and store data
    h1_tag = soup.find('h1')
    if h1_tag:
        text = h1_tag.get_text(strip=True)
        names.append(text)
    else:
        print("No <h1> tag found.")
    
    img_tag = page.query_selector('img.wp-post-image')
    if img_tag:
        src = img_tag.get_attribute('src')
        if src:
            image_URL.append(src)
        else:
            print("No src attribute found.")
    else:
        print("No image tag found.")
    
    p_tag = page.query_selector('#tab-description')
    if p_tag:
        p_text = p_tag.text_content()
        if p_text:
            Description.append(p_text)
        else:
            print("Can't find description.")
    else:
        print("No <p> tag found.")
    
def process_class_name(page, class_name):
    lists.clear()  # Clear previous lists
    list2.clear()
    
    # Wait for the class name div to be loaded and visible
    page.wait_for_selector(f'.{class_name}')
    
    # Find all h2 tags within the specified class name div
    h2_tags = page.query_selector_all(f'.{class_name} h2')
    for h2 in h2_tags:
        h2_text = h2.text_content().strip()
        lists.append(h2_text)
    
    # Click the parent div containing each h2 text
    for h2_text in lists:
        try:
            # Find the parent div of the h2 tag
            parent_div = page.query_selector(f'.{class_name} h2:text("{h2_text}") >> ..')
            
            if parent_div:
                parent_div.click()
                page.wait_for_timeout(500)
                
                # Extract product names and click each
                h2_tagss = page.query_selector_all('.products.columns-4 h2')
                for h2 in h2_tagss:
                    h2_text = h2.text_content().strip()
                    list2.append(h2_text)
                
                for h2_text in list2:
                    parent_div = page.query_selector(f'.products.columns-4 h2:text("{h2_text}") >> ..')
                    if parent_div:
                        parent_div.click()
                        page.wait_for_timeout(1000)
                        scrape_data(page)
                        page.go_back()
                        page.wait_for_timeout(500)
                
                page.go_back()
            else:
                print(f"No div found containing: {h2_text}")
            
            # Optionally, add a short delay to avoid rapid clicks if needed
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f"Error interacting with div: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto(link)
    # Click on the sixth product item and wait for the page to load
    page.click('//*[@id="content"]/div/div/div/ul/li[6]/a/img')
    page.wait_for_load_state("networkidle")  # Wait until the page has finished loading
    
    # Call the function with the class name
    process_class_name(page, 'col-md-12')
    browser.close()

# Debug: Print lengths of lists
print(f"Names length: {len(names)}")
print(f"Image URLs length: {len(image_URL)}")
print(f"Descriptions length: {len(Description)}")

# Ensure all lists are of the same length
if len(names) == len(image_URL) == len(Description):
    df = pd.DataFrame({
        'Names': names,
        'Description': Description,
        'Image_URL': image_URL
    })
    df.to_csv('sheet2.csv', index=False)
else:
    print("Data lists have different lengths. Check the data extraction process.")
