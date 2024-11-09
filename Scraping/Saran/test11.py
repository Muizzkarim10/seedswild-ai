import pandas as pd
from playwright.sync_api import sync_playwright
import time

link = "https://www.parkseed.com/herbs?p=3"
names = []
image_URL1 = []
Mature_Height = []
Mature_Width = []
sun = []
bloom_size = []
habit = []
Genus = []
Species = []
Variety = []
Product = []
Sun_Shade = []
Bloom_Start = []
Bloom_End = []
Bloom_Color = []
Habit= []
Foliage_Color = []
Resistance = []
Characteristics = []
Uses = []
Zone = []

def safe_click(page, selector):
    retries = 3
    while retries > 0:
        try:
            element = page.locator(selector)
            if element.is_visible():
                element.click()
                return True
            time.sleep(1)  # Wait before retrying
        except Exception as e:
            print(f"Retrying due to exception: {e}")
            time.sleep(1)
        retries -= 1
    return False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(link)
    
    forms = page.locator('//*[@id="product-list"]/div[2]/div/form')
    form_count = forms.count()

    for index in range(form_count):
        # Ensure to select each form individually
        form_selector = f'//*[@id="product-list"]/div[2]/div/form[{index + 1}]'
        if safe_click(page, form_selector):
            page.wait_for_timeout(4000)  # Adjust as needed

            try:
                h1_tag = page.locator('//*[@id="maincontent"]/div[3]/div/div[1]/section[1]/div/div/div[1]/h1/span')
                names.append(h1_tag.text_content() or "N/A")
            except Exception as e:
                print(f"Error retrieving <h1> tag: {e}")
                names.append("N/A")
            img1 = page.locator('//*[@id="gallery"]/div/div[1]/div/img[2]')
            src1 = img1.get_attribute('src') or "N/A"
            image_URL1.append(src1)
            try:
                height = page.locator('//*[@id="maincontent"]/div[3]/div/div[1]/section[3]/div/div[2]/div[1]/div[2]/h3')
                Mature_Height.append(height.text_content() or "N/A")
                width = page.locator('//*[@id="maincontent"]/div[3]/div/div[1]/section[3]/div/div[2]/div[2]/div[2]/h3')
                Mature_Width.append(width.text_content() or "N/A")
                shade = page.locator('//*[@id="maincontent"]/div[3]/div/div[1]/section[3]/div/div[2]/div[3]/div[2]/h3')
                sun.append(shade.text_content() or "N/A")
                bloom = page.locator('//*[@id="maincontent"]/div[3]/div/div[1]/section[3]/div/div[2]/div[4]/div[2]/h3')
                bloom_size.append(bloom.text_content() or "N/A")
                habitat = page.locator('//*[@id="maincontent"]/div[3]/div/div[1]/section[3]/div/div[2]/div[5]/div[2]/h3')
                habit.append(habitat.text_content() or "N/A")
            except Exception as e:
                print(f"Error retrieving attributes: {e}")
                Mature_Height.append("N/A")
                Mature_Width.append("N/A")
                sun.append("N/A")
                bloom_size.append("N/A")
                habit.append("N/A")
            
            try:
                genuss = page.locator('//*[@id="product-attributes"]/table/tbody/tr[1]/td')
                Genus.append(genuss.text_content() or "N/A")
                species = page.locator('//*[@id="product-attributes"]/table/tbody/tr[2]/td')
                Species.append(species.text_content() or "N/A")
                variety = page.locator('//*[@id="product-attributes"]/table/tbody/tr[3]/td')
                Variety.append(variety.text_content() or "N/A")
                product = page.locator('//*[@id="product-attributes"]/table/tbody/tr[4]/td')
                Product.append(product.text_content() or "N/A")
                sun_shade = page.locator('//*[@id="product-attributes"]/table/tbody/tr[5]/td')
                Sun_Shade.append(sun_shade.text_content() or "N/A")
                bloom_season = page.locator('//*[@id="product-attributes"]/table/tbody/tr[6]/td')
                Bloom_Start.append(bloom_season.text_content() or "N/A")
                bloom_end = page.locator('//*[@id="product-attributes"]/table/tbody/tr[7]/td')
                Bloom_End.append(bloom_end.text_content() or "N/A")
                bloom_color = page.locator('//*[@id="product-attributes"]/table/tbody/tr[8]/td')
                Bloom_Color.append(bloom_color.text_content() or "N/A")
                foliage = page.locator('//*[@id="product-attributes"]/table/tbody/tr[9]/td')
                Foliage_Color.append(foliage.text_content() or "N/A")
                habitt = page.locator('//*[@id="product-attributes"]/table/tbody/tr[10]/td')
                Habit.append(habitt.text_content() or "N/A")
                resistance = page.locator('//*[@id="product-attributes"]/table/tbody/tr[11]/td')
                Resistance.append(resistance.text_content() or "N/A")
                xhar = page.locator('//*[@id="product-attributes"]/table/tbody/tr[12]/td')
                Characteristics.append(xhar.text_content() or "N/A")
                uses = page.locator('//*[@id="product-attributes"]/table/tbody/tr[13]/td')
                Uses.append(uses.text_content() or "N/A")
                zone = page.locator('//*[@id="product-attributes"]/table/tbody/tr[14]/td')
                Zone.append(zone.text_content() or "N/A")
            except Exception as e:
                print(f"Error retrieving attributes from product attributes table: {e}")
                Genus.append("N/A")
                Species.append("N/A")
                Variety.append("N/A")
                Product.append("N/A")
                Sun_Shade.append("N/A")
                Bloom_Start.append("N/A")
                Bloom_End.append("N/A")
                Bloom_Color.append("N/A")
                Foliage_Color.append("N/A")
                Habit.append("N/A")
                Resistance.append("N/A")
                Characteristics.append("N/A")
                Uses.append("N/A")
                Zone.append("N/A")

            # Go back to the previous page
            page.go_back()
            # Wait for the page to load after navigation
            page.wait_for_timeout(2000)  # Adjust as needed

            # Reload the forms after going back
            forms = page.locator('//*[@id="product-list"]/div[2]/div/form')
            form_count = forms.count()

        else:
            print("Failed to click form after several retries.")

        # # Optional: print information after processing each form
        # print("Mature Height:", Mature_Height)
        # print("Mature Width:", Mature_Width)
        # print("Sun:", sun)
        # print("Bloom Size:", bloom_size)
        # print("Habit:", habit)
        # print("Image URLs 1:", image_URL1)
        # print("Names:", names)
        # print("Genus:", Genus)
        # print("Species:", Species)
        # print("Variety:", Variety)
        # print("Product:", Product)
        # print("Sun/Shade:", Sun_Shade)
        # print("Bloom Season Start:", Bloom_Start)
        # print("Bloom Season End:", Bloom_End)
        # print("Bloom Color:", Bloom_Color)
        # print("Foliage Color:", Foliage_Color)
        # print("Habit:", Habit)
        # print("Resistance:", Resistance)
        # print("Characteristics:", Characteristics)
        # print("Uses:", Uses)
        # print("Zone:", Zone)

    browser.close()

# Create DataFrame and save to CSV
max_length = max(len(names), len(image_URL1),
                  len(Mature_Height), len(Mature_Width), len(sun), len(bloom_size),
                  len(habit), len(Genus), len(Species), len(Variety), len(Product),
                  len(Sun_Shade), len(Bloom_Start), len(Bloom_End), len(Bloom_Color),
                  len(Foliage_Color), len(Habit), len(Resistance), len(Characteristics),
                  len(Uses), len(Zone))

# Pad lists with NaN values
def pad_list(lst, length):
    return lst + [None] * (length - len(lst))

names = pad_list(names, max_length)
image_URL1 = pad_list(image_URL1, max_length)
Mature_Height = pad_list(Mature_Height, max_length)
Mature_Width = pad_list(Mature_Width, max_length)
sun = pad_list(sun, max_length)
bloom_size = pad_list(bloom_size, max_length)
habit = pad_list(habit, max_length)
Genus = pad_list(Genus, max_length)
Species = pad_list(Species, max_length)
Variety = pad_list(Variety, max_length)
Product = pad_list(Product, max_length)
Sun_Shade = pad_list(Sun_Shade, max_length)
Bloom_Start = pad_list(Bloom_Start, max_length)
Bloom_End = pad_list(Bloom_End, max_length)
Bloom_Color = pad_list(Bloom_Color, max_length)
Foliage_Color = pad_list(Foliage_Color, max_length)
Habit = pad_list(Habit, max_length)
Resistance = pad_list(Resistance, max_length)
Characteristics = pad_list(Characteristics, max_length)
Uses = pad_list(Uses, max_length)
Zone = pad_list(Zone, max_length)

# Create DataFrame
df = pd.DataFrame({
    'Name': names,
    'Image URL 1': image_URL1,
    'Mature Height': Mature_Height,
    'Mature Width': Mature_Width,
    'Sun': sun,
    'Bloom Size': bloom_size,
    'Habit': habit,
    'Genus': Genus,
    'Species': Species,
    'Variety': Variety,
    'Product': Product,
    'Sun/Shade': Sun_Shade,
    'Bloom Season Start': Bloom_Start,
    'Bloom Season End': Bloom_End,
    'Bloom Color': Bloom_Color,
    'Foliage Color': Foliage_Color,
    'Habit': Habit,
    'Resistance': Resistance,
    'Characteristics': Characteristics,
    'Uses': Uses,
    'Zone': Zone
})

df.to_csv('sheet3.csv', index=False)

