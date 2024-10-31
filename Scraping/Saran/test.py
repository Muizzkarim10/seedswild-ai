import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

link = "https://americanseedco.com/"
names = []
image_URL = []
Description = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto(link)
    page.click('ul.products > li:nth-child(6)')
    page.wait_for_timeout(1000)  # Wait for navigation

    for i in range(1, 15):
        li_selector = f'ul.products > li:nth-child({i})'
        try:
            page.click(li_selector)
            page.wait_for_timeout(500)
            li_element = page.query_selector_all('ul.products > li')
            length = len(li_element)
            for j in range(1, length + 1): 
                nested_li_selector = f'ul.products > li:nth-child({j})'
                try:
                    page.click(nested_li_selector)
                    page.wait_for_timeout(500)
                    html = page.inner_html('#content')
                    soup = BeautifulSoup(html, 'html.parser')
                    h1_tag = soup.find('h1')
                    if h1_tag:
                        text = h1_tag.get_text(strip=True)
                        names.append(text)
                    else:
                        print("No <h1> tag found.")

                    image = 'img.wp-post-image'
                    src = page.get_attribute(image, 'src')
                    if src:
                        image_URL.append(src)
                    else:
                        print("No src tag found.")

                    p_tag = page.locator('#tab-description')
                    p_text = p_tag.text_content()
                    if p_text:
                        Description.append(p_text)
                    else:
                        print("Can't find description.")
                    
                    page.go_back()  # Go back after each inner item is clicked
                except Exception as e:
                    pass

            page.go_back()
            page.wait_for_timeout(1000)
        except Exception as e:
            pass

    page.go_back()      
    page.click('ul.products > li:nth-child(9)')
    page.wait_for_timeout(1000)  # Wait for navigation

    for i in range(1, 4):
        li_selector = f'ul.products > li:nth-child({i})'
        try:
            page.click(li_selector)
            page.wait_for_timeout(500)
            li_element = page.query_selector_all('ul.products > li')
            length = len(li_element)
            for j in range(1, length + 1): 
                nested_li_selector = f'ul.products > li:nth-child({j})'
                page.click(nested_li_selector)
                page.wait_for_timeout(500)
                html = page.inner_html('#content')
                soup = BeautifulSoup(html, 'html.parser')
                h1_tag = soup.find('h1')
                if h1_tag:
                    text = h1_tag.get_text(strip=True)
                    names.append(text)
                else:
                    print("No <h1> tag found.")

                image = 'img.wp-post-image'
                src = page.get_attribute(image, 'src')
                if src:
                   image_URL.append(src)
                else:
                   print("No src tag found.")

                p_tag = page.locator('#tab-description')
                p_text = p_tag.text_content()
                if p_text:
                    Description.append(p_text)
                else:
                    print("Can't find description.")
                    
                page.go_back()  # Go back after each inner item is clicked
                page.wait_for_timeout(1000)
            try:
                page.click('.next.page-numbers')
                page.wait_for_timeout(1000)
                for k in range(1,14):
                    li_selector = f'ul.products > li:nth-child({k})'
                    page.click(li_selector)
                    page.wait_for_timeout(1000)
                    html = page.inner_html('#content')
                    soup = BeautifulSoup(html, 'html.parser')
                    # Extract and store data
                    h1_tag = soup.find('h1')
                    if h1_tag:
                      text = h1_tag.get_text(strip=True)
                      names.append(text)
                    else:
                      print("No <h1> tag found.")
                    image = 'img.wp-post-image'
                    src = page.get_attribute(image, 'src')
                    if src:
                       image_URL.append(src)
                    else:
                      print("No src tag found.")
                    p_tag = page.locator('#tab-description')
                    p_text = p_tag.text_content()
                    if p_text:
                      Description.append(p_text)
                    else:
                      print("Can't find description.")
                    page.go_back()
                    page.wait_for_timeout(1000)  # Go back after processing each item
                break
            except:
                page.go_back()
                page.wait_for_timeout(1000)

        except Exception as e:
            pass

    page.go_back()
   
    page.wait_for_timeout(500)
    page.click('ul.products > li:nth-child(20)')

    for i in range(1, 21):
        li_selector = f'ul.products > li:nth-child({i})'
        try:
            page.click(li_selector)
            page.wait_for_timeout(1000)
            
            html = page.inner_html('#content')
            soup = BeautifulSoup(html, 'html.parser')

            # Extract and store data
            h1_tag = soup.find('h1')
            if h1_tag:
                text = h1_tag.get_text(strip=True)
                names.append(text)
            else:
                print("No <h1> tag found.")

            image = 'img.wp-post-image'
            src = page.get_attribute(image, 'src')
            if src:
                image_URL.append(src)
            else:
                print("No src tag found.")

            p_tag = page.locator('#tab-description')
            p_text = p_tag.text_content()
            if p_text:
                Description.append(p_text)
            else:
                print("Can't find description.")
            
            page.go_back()  # Go back after processing each item
            
        except Exception as e:
            print(f"An error occurred while processing item {i}: {e}")
            page.go_back()  # Ensure navigation back even if an error occurs

    # Navigate to the next page
    page.click('.next.page-numbers')
    page.wait_for_timeout(1000)  # Wait for navigation
        
    for j in range(1, 9):
        li_selector = f'ul.products > li:nth-child({j})'
        page.click(li_selector)
        page.wait_for_timeout(1000)
                
        html = page.inner_html('#content')
        soup = BeautifulSoup(html, 'html.parser')

        # Extract and store data
        h1_tag = soup.find('h1')
        if h1_tag:
            text = h1_tag.get_text(strip=True)
            names.append(text)
        else:
            print("No <h1> tag found.")

        image = 'img.wp-post-image'
        src = page.get_attribute(image, 'src')
        if src:
            image_URL.append(src)
        else:
            print("No src tag found.")
        p_tag = page.locator('#tab-description')
        p_text = p_tag.text_content()
        if p_text:
            Description.append(p_text)
        else:
            print("Can't find description.")
        
        page.go_back()  # Go back after processing each item
    page.wait_for_timeout(500)
    page.click('ul.products > li:nth-child(5)')

    for i in range(1, 21):
        li_selector = f'ul.products > li:nth-child({i})'
        try:
            page.click(li_selector)
            page.wait_for_timeout(1000)
            
            html = page.inner_html('#content')
            soup = BeautifulSoup(html, 'html.parser')

            # Extract and store data
            h1_tag = soup.find('h1')
            if h1_tag:
                text = h1_tag.get_text(strip=True)
                names.append(text)
            else:
                print("No <h1> tag found.")

            image = 'img.wp-post-image'
            src = page.get_attribute(image, 'src')
            if src:
                image_URL.append(src)
            else:
                print("No src tag found.")

            p_tag = page.locator('#tab-description')
            p_text = p_tag.text_content()
            if p_text:
                Description.append(p_text)
            else:
                print("Can't find description.")
            
            page.go_back()  # Go back after processing each item
            
        except Exception as e:
            print(f"An error occurred while processing item {i}: {e}")
            page.go_back()  # Ensure navigation back even if an error occurs

    # Navigate to the next page
    page.click('.next.page-numbers')
    page.wait_for_timeout(1000)  # Wait for navigation
        
    for j in range(1, 5):
        li_selector = f'ul.products > li:nth-child({j})'
        page.click(li_selector)
        page.wait_for_timeout(1000)
                
        html = page.inner_html('#content')
        soup = BeautifulSoup(html, 'html.parser')

        # Extract and store data
        h1_tag = soup.find('h1')
        if h1_tag:
            text = h1_tag.get_text(strip=True)
            names.append(text)
        else:
            print("No <h1> tag found.")

        image = 'img.wp-post-image'
        src = page.get_attribute(image, 'src')
        if src:
            image_URL.append(src)
        else:
            print("No src tag found.")
        p_tag = page.locator('#tab-description')
        p_text = p_tag.text_content()
        if p_text:
            Description.append(p_text)
        else:
            print("Can't find description.")
        
        page.go_back()  # Go back after processing each item
    page.click('ul.products > li:nth-child(11)')
    for i in range(1, 21):
        li_selector = f'ul.products > li:nth-child({i})'
        try:
            page.click(li_selector)
            page.wait_for_timeout(1000)
            
            html = page.inner_html('#content')
            soup = BeautifulSoup(html, 'html.parser')

            # Extract and store data
            h1_tag = soup.find('h1')
            if h1_tag:
                text = h1_tag.get_text(strip=True)
                names.append(text)
            else:
                print("No <h1> tag found.")

            image = 'img.wp-post-image'
            src = page.get_attribute(image, 'src')
            if src:
                image_URL.append(src)
            else:
                print("No src tag found.")

            p_tag = page.locator('#tab-description')
            p_text = p_tag.text_content()
            if p_text:
                Description.append(p_text)
            else:
                print("Can't find description.")
            
            page.go_back()  # Go back after processing each item
            
        except Exception as e:
            print(f"An error occurred while processing item {i}: {e}")
            page.go_back()  # Ensure navigation back even if an error occurs
    
    page.go_back()  # Go back after each inner item is clicked
    df =pd.DataFrame({
        'Name' : names,
        'Description' : Description,
        'Image_URL' : image_URL
    })
    df.to_csv('data1')
    browser.close()
