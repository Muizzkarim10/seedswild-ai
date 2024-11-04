import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Target URL containing the list of products
link = "https://www.johnnyseeds.com/farm-seed/legumes/"

# Lists to store extracted data
names = []
image_URL1 = []
image_URL2 = []
image_URL3 = []
descriptions = []

with sync_playwright() as p:
    # Launch the browser
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    
    # Navigate to the main page
    page.goto(link)
    
    # Wait for the product grid to load
    page.wait_for_timeout(10000)
    
    # Retrieve all product tiles
    product_tiles = page.locator('.product-grid .product-tile')
    count = product_tiles.count()
    
    print(f"Found {count} product tiles.")
    
    for i in range(count):
        # Select the i-th product tile
        tile = product_tiles.nth(i)
        
        try:
            # Extract the product link
            tile_link = tile.locator('a').first
            href = tile_link.get_attribute('href')
            
            if href is None:
                print(f"No href found for product tile {i+1}. Skipping.")
                continue
            else:
                print(f"Navigating to {href}")
                # Navigate to the product detail page
                page.goto(href)
        except Exception as e:
            print(f"Error retrieving link for product tile {i+1}: {e}")
            continue
        
        # Wait for the page to fully load
        page.wait_for_load_state('load')
        
        # Retrieve the page's HTML content
        page_content = page.content()
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Extract the product name
        h1_tag = soup.select_one('h1.product-name')
        if h1_tag:
            product_name = h1_tag.get_text(strip=True)
            names.append(product_name)
        else:
            print(f"No product name found for product {i+1}.")
            names.append("N/A")
        
        # Extract product images
        image_tags = soup.select('div.primary-images img')
        if image_tags:
            num_images = len(image_tags)
            print(f"Found {num_images} images for product {i+1}.")
            
            # Initialize image URLs
            src1 = src2 = src3 = "N/A"
            
            if num_images >= 1:
                src1 = image_tags[0].get('src', "N/A")
            if num_images >= 2:
                src2 = image_tags[1].get('src', "N/A")
            if num_images >= 3:
                src3 = image_tags[2].get('src', "N/A")
            
            image_URL1.append(src1)
            image_URL2.append(src2)
            image_URL3.append(src3)
        else:
            print(f"No images found for product {i+1}.")
            image_URL1.append("N/A")
            image_URL2.append("N/A")
            image_URL3.append("N/A")
        
        # Extract product description
        desc_div = soup.select_one('#collapsible-details-1')
        if desc_div:
            desc_text = desc_div.get_text(strip=True)
            descriptions.append(desc_text)
        else:
            print(f"No description found for product {i+1}.")
            descriptions.append("N/A")
        
        # Navigate back to the main page
        page.go_back()
        page.wait_for_load_state('load')
    
    # Close the browser
    browser.close()

# Create a DataFrame to store the extracted data
df = pd.DataFrame({
    'Names': names,
    'Description': descriptions,
    'Image_URL1': image_URL1,
    'Image_URL2': image_URL2,
    'Image_URL3': image_URL3
})

# Save the DataFrame to a CSV file
df.to_csv('sheet5.csv', index=False)
