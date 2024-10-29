import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

link = "https://www.sativa.bio/en/vegetables/cress"
names = []
image_URL1 = []
image_URL2 = []
image_URL3 = []
Description = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto(link)
    
    for i in range(1, 26):
        li_selector = f'ol.products.list.items.product-items > li:nth-child({i})'
        page.click(li_selector)
        page.wait_for_timeout(10000)
        
        html = page.inner_html('#maincontent')
        soup = BeautifulSoup(html, 'html.parser')
        
        h1_tag = soup.find('h1')
        if h1_tag:
            text = h1_tag.get_text(strip=True)
            names.append(text)
        else:
            print("No <h1> tag found.")
        
        # Wait for the images to be visible and then get their src attributes
        image_selector = 'img.fotorama__img'
        try:
            page.wait_for_selector(image_selector, timeout=10000)  # Wait for images to load
            images = page.locator(image_selector).all()  # Get all matching images
            if len(images) >= 3:  # Check if there are at least 3 images
                src1 = images[0].get_attribute('src')
                src2 = images[1].get_attribute('src')
                src3 = images[2].get_attribute('src')
                
                if src1:
                    image_URL1.append(src1)
                else:
                    image_URL1.append("No src found for image 1")
                
                if src2:
                    image_URL2.append(src2)
                else:
                    image_URL2.append("No src found for image 2")
                
                if src3:
                    image_URL3.append(src3)
                else:
                    image_URL3.append("No src found for image 3")
            else:
                print(f"Less than 3 images found for item {i}")
                image_URL1.append("Not enough images")
                image_URL2.append("Not enough images")
                image_URL3.append("Not enough images")
        
        except Exception as e:
            print(f"Error retrieving image src: {e}")
            image_URL1.append("Error")
            image_URL2.append("Error")
            image_URL3.append("Error")
        
        p_tag = page.locator('p[itemprop="description"]')
        p_text = p_tag.text_content()
        if p_text:
            Description.append(p_text)
        else:
            print("Can't find description.")
        
        page.go_back()

# Create a DataFrame with three image URL columns
df = pd.DataFrame({
    'Names': names,
    'Description': Description,
    'Image_URL1': image_URL1,
    'Image_URL2': image_URL2,
    'Image_URL3': image_URL3
})
df.to_csv('sheet2.csv', index=False)
