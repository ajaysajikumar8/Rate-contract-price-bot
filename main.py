# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from dotenv import load_dotenv
from websites import websites
from search_product import search_product
import os
from utils import setup_logging

setup_logging('main.log')

chrome_options = Options()
load_dotenv()

headers = {
    "User-Agent": os.getenv("USER_AGENT"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE"),
    "Accept": os.getenv("ACCEPT"),
    "Accept-Encoding": os.getenv("ACCEPT_ENCODING"),
}

for key, value in headers.items():
    chrome_options.add_argument(f"--header={key}: {value}")

def scrape_website(driver, website_info, product_name):
    site, product, price = search_product(
        driver,
        website_info,
        product_name
    )
    return site, product, price

def main():
    product_name = input("Enter the product you are searching for: ")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        for website_info in websites:
            site, product, price = scrape_website(driver, website_info, product_name)
            print("\nPrices for '{}' on {}:".format(product, site))
            print("Price:", price)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
