# search_product.py
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils import wait_and_get_element, setup_logging
from find_similar_item import find_similar_item
import logging

setup_logging("search_product.log")


def search_product(driver, website, product):
    try:
        driver.get(website["url"])
        search_bar = wait_and_get_element(driver, website["search_bar_locator"])
        search_bar.clear()
        search_bar.send_keys(product)
        search_bar.send_keys(Keys.RETURN)
        
        try:
            first_item = wait_and_get_element(driver, website["first_item_locator"])
        except NoSuchElementException as e:
            logging.debug(
                f'NoSuchElementException: {e}, Website: {website["url"]}, Product: {product}'
            )
            print("First Element not found")
            return website["url"], "No matching product found", "Price not found"

        site, product_name, price = find_similar_item(website, product, first_item)

        return site, product_name, price
    
    except TimeoutException as e:
        logging.debug(
            f"TimeoutException occurred while trying to fetch product name on {website['url']}."
        )
        print("Timeout")
        return website["url"], "No matching product found", "Price not found"
