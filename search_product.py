# search_product.py
from selenium.webdriver.common.keys import Keys
from utils import *
import time

def search_product(driver, website, product):
    driver.get(website["url"])

    search_bar = wait_and_get_element(driver, website["search_bar_locator"])
    search_bar.clear()
    search_bar.send_keys(product)
    search_bar.send_keys(Keys.RETURN)

    # Wait for the search results to load (adjust the sleep time as needed)
    time.sleep(5)

    # Locate the first item within the search results
    first_item = wait_and_get_element(driver, website["first_item_locator"])

    if website["url"] == "https://www.amazon.in":
        if 'AdHolder' not in first_item.get_attribute('class'):
            product_name_element = wait_and_get_element_by_class_name(driver, website["product_name_locator"][1])
            product_name = product_name_element.text
            price_element = wait_and_get_element_by_class_name(driver, website["price_locator"][1])
            price = price_element.text if price_element else 'Price not found' 
        else:
            print("The first item is sponsored. Looking for a non-sponsored element.")
            sibling_item = first_item
            while sibling_item:
                sibling_item = wait_and_get_element_by_xpath_relative(sibling_item, './following-sibling::*')

                if 'AdHolder' not in sibling_item.get_attribute('class'):
                    print("Found a non-sponsored element among siblings.")
                    product_name_element = wait_and_get_element_by_class_name_relative(sibling_item, website["product_name_locator"][1])
                    product_name = product_name_element.text if product_name_element else "Name not found"
                    price_element = wait_and_get_element_by_class_name_relative(sibling_item, website["price_locator"][1])
                    price = price_element.text if price_element else 'Price not found'
                    break
    else:
        product_name_element = wait_and_get_element_by_class_name_relative(first_item, website["product_name_locator"][1])
        product_name = product_name_element.text
        price_element = wait_and_get_element_by_class_name_relative(first_item, website["price_locator"][1])
        price = price_element.text if price_element else 'Price not found' 
        
    return website["url"], product_name, price
