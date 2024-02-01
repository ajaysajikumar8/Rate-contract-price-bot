from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
import os

chrome_options = Options()
load_dotenv()


headers = {
    "User-Agent" : os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE"),
    "Accept": os.getenv("ACCEPT"),
    "Accept-Encoding": os.getenv("ACCEPT_ENCODING"),
}

for key, value in headers.items():
    chrome_options.add_argument(f"--header={key}: {value}")

CHROMEDRIVER_PATH = "D:\chrome-win64\chrome.exe"



def search_product(driver, website, product, search_bar_locator, first_item_locator, price_locator):
    driver.get(website)

    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(search_bar_locator)
    )
    search_bar.clear()
    search_bar.send_keys(product)
    search_bar.send_keys(Keys.RETURN)

    # Wait for the search results to load (adjust the sleep time as needed)
    time.sleep(5)

    # Locate the first item within the search results
    first_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(first_item_locator)
    )

    if website == "https://www.amazon.in":
        if 'AdHolder' not in first_item.get_attribute('class'):
            price_element = first_item.find_element(By.CLASS_NAME, price_locator[1])
            price = price_element.text if price_element else 'Price not found' 
            print(price)
        else:
            print("The first item is sponsored. Looking for a non-sponsored element.")
            sibling_item = first_item
            while sibling_item:
                sibling_item = sibling_item.find_element(By.XPATH, './following-sibling::*')

                if 'AdHolder' not in sibling_item.get_attribute('class'):
                    print("Found a non-sponsored element among siblings.")
                    price_element = sibling_item.find_element(By.CLASS_NAME, price_locator[1])
                    price = price_element.text if price_element else 'Price not found'
                    print(price)
                    break
    else:
        price_element = first_item.find_element(By.XPATH, price_locator[1])
        price = price_element.text if price_element else 'Price not found' 
        print(price)
    return website, price



def scrape_website(driver, website_info, product_name):
    site, price = search_product(
        driver,
        website_info['url'],
        product_name,
        website_info['search_bar_locator'],
        website_info['first_item_locator'],
        website_info['price_locator']
    )
    return site, price

def main():
    product_name = input("Enter the product you are searching for: ")

    websites = [
        {
            'url': 'https://www.amazon.in',
            'search_bar_locator': ('xpath', '//*[@id="twotabsearchtextbox"]'),
            'first_item_locator': ('xpath', '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]'),
            'price_locator': ('CLASS_NAME', 'a-price-whole'),
        },
        {
            'url': 'https://www.flipkart.com',
            'search_bar_locator': ('xpath', '//*[@id="container"]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div/div[1]/div[1]/header/div[1]/div[2]/form/div/div/input'),
            'first_item_locator': ('xpath', '//*[@id="container"]/div/div[3]/div/div[2]/div[2]'),
            'price_locator': ('xpath', './div/div/div/a/div[2]/div[2]/div[1]/div/div[1]'),
        },
        {
            'url': 'https://www.flipkart.com',
            'search_bar_locator': ('xpath', '//*[@id="container"]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div/div[1]/div[1]/header/div[1]/div[2]/form/div/div/input'),
            'first_item_locator': ('xpath', '//*[@id="container"]/div/div[3]/div/div[2]/div[2]'),
            'price_locator': ('xpath', './div/div/div/a/div[2]/div[2]/div[1]/div/div[1]'),
        }
        
        # Add more websites and their rules as needed
    ]

    product_prices = {}

    driver = webdriver.Chrome(options=chrome_options)

    try:
        for website_info in websites:
            site, price = scrape_website(driver, website_info, product_name)
            product_prices[site] = price

        print("\nPrices for '{}' on different websites:".format(product_name))
        for website, price in product_prices.items():
            print("{}: {}".format(website, price))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
