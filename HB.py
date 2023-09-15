import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Getting links for each bundle in the games page
driver = webdriver.Chrome()
driver.get('https://www.humblebundle.com/games')

Links = driver.find_elements(By.CLASS_NAME, "full-tile-view")
link_list = []
for link in Links:
    link_url = link.get_attribute("href")
    if link_url:
        link_list.append(link_url)

driver.quit()

# CSV file creation
with open('humble_bundles.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'Bundle Name',
        'Bundle Title',
        'Bundle Description',
        'Sold',
        'Redeem on Steam',
        'Platform / OS',
        'Charity Amount Raised',
        'Bundle Value',
        'Countdown Value',
        'Price',
        'Number of Items'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # CSV header
    writer.writeheader()

    # Scraping i guess
    for Link in link_list:

        # Selenium magic
        driver = webdriver.Chrome()
        driver.get(Link)

        # Getting bundle name
        bundle_name = driver.title

        # Getting title of the description
        bundle_title = driver.find_element(By.CSS_SELECTOR, '#mm-0 > div.page-wrap > div.base-main-wrapper > div.inner-main-wrapper > div > div:nth-child(1) > div.sidebar > div > div.js-basic-info-view > div > h2')

        # Getting description
        bundle_description = driver.find_element(By.CLASS_NAME, "marketing-blurb")

        # Getting facts
        # Sold
        sold = driver.find_element(By.CSS_SELECTOR, '#mm-0 > div.page-wrap > div.base-main-wrapper > div.inner-main-wrapper > div > div:nth-child(1) > div.sidebar > div > div.js-basic-info-view > div > section.quick-facts > div:nth-child(2) > span')

        # Redeem on Steam
        steam = driver.find_element(By.CSS_SELECTOR, '#mm-0 > div.page-wrap > div.base-main-wrapper > div.inner-main-wrapper > div > div:nth-child(1) > div.sidebar > div > div.js-basic-info-view > div > section.quick-facts > div:nth-child(3) > span')

        # Platform / OS
        OS = driver.find_element(By.CSS_SELECTOR, '#mm-0 > div.page-wrap > div.base-main-wrapper > div.inner-main-wrapper > div > div:nth-child(1) > div.sidebar > div > div.js-basic-info-view > div > section.quick-facts > div:nth-child(4) > span')

        # Getting charity amount raised
        bundle_charity_amount_raised = driver.find_element(By.CLASS_NAME, "charity-amount-raised")
        C = re.search(r'US\$(\d{1,3}(?:,\d{3})*)(?:\.\d{2})?', bundle_charity_amount_raised.text)
        
        # Getting bundle value
        bundle_value = driver.find_element(By.CSS_SELECTOR, '#mm-0 > div.page-wrap > div.base-main-wrapper > div.inner-main-wrapper > div > div:nth-child(1) > div.sidebar > div > div.js-pwyw-view > div > h2')
        V = re.search(r'US\$(\d{1,3}(?:,\d{3})*)(?:\.\d{2})?', bundle_value.text)
        
        # Getting Offer ends in
        bundle_ends = driver.find_element(By.CLASS_NAME, "js-countdown")
        countdown_value = re.search(r'(\d+ days : \d+ hours : \d+ minutes)', bundle_ends.text).group(1)

        # Getting Bundle Price and items number
        bundle_price_items = driver.find_element(By.CLASS_NAME, 'js-tier-header')
        bundle = str(bundle_price_items.text)
        P = re.search(r'US\$(\d{1,3}(?:,\d{3})*)(?:\.\d{2})?', bundle)
        I = re.search(r'(\d+)\s+items', bundle)

        # CSV file data writing
        writer.writerow({
            'Bundle Name': bundle_name,
            'Bundle Title': bundle_title.text,
            'Bundle Description': bundle_description.text,
            'Sold': sold.text,
            'Redeem on Steam': steam.text,
            'Platform / OS': OS.text,
            'Charity Amount Raised': C.group(1) if C else '',
            'Bundle Value': V.group(1) if V else '',
            'Countdown Value': countdown_value,
            'Price': P.group(1) if P else '',
            'Number of Items': I.group(1) if I else ''
        })

        driver.quit()
# 0xAK
