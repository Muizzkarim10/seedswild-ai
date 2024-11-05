import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://pk.indeed.com/")
    page.get_by_role("link", name="Sign in").click()
    page.get_by_label("Email address *").click()
    page.get_by_label("Email address *").click()
    page.get_by_label("Email address *").fill("post4msaran@gmail.com")
    page.get_by_role("button", name="Continue", exact=True).click()
    page.get_by_role("link", name="Sign in with login code").click()
    page.get_by_label("Enter 6-digit code *").click()
    page.wait_for_timeout(10000)
    # page.get_by_label("Enter 6-digit code *").fill("645395")
    page.get_by_label("Enter 6-digit code *").press("Enter")
    page.get_by_role("link", name="Skip").click()
    page.get_by_test_id("page").click()
    page.get_by_text("Employers can't see this.").click()
    page.get_by_role("link", name="Skip").click()
    page.get_by_role("link", name="Skip").click()

    
