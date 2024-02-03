from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from utils import wait_and_get_element_by_class_name_relative, wait_and_get_element_by_xpath_relative, setup_logging
import time
import logging
from fuzzywuzzy import fuzz


setup_logging("find_similar_item.log")

def find_similar_item(website, product, first_item):
    max_similarity_score = 0
    max_similarity_item = None
    sibling_item = first_item

    class_names_set1 = website["product_name_locator"][0][1]
    class_names_set2 = website["product_name_locator"][1][1]

    def get_product_name_element(sibling_item, class_names):
        try:
            return wait_and_get_element_by_class_name_relative(sibling_item, class_names)
        except NoSuchElementException as e:
            logging.debug(
                f'NoSuchElementException: {e}, Website: {website["url"]}, Product: {product}'
            )
            return None

    def get_price_element(item):
        try:
            return wait_and_get_element_by_class_name_relative(item, website["price_locator"][1])
        except NoSuchElementException as e:
            return None

    for _ in range(6):  # Fetch product names for the first 6 items
        try:
            product_name_element = get_product_name_element(sibling_item, class_names_set1)

            if product_name_element is None:
                product_name_element = get_product_name_element(sibling_item, class_names_set2)

            product_name = product_name_element.text if product_name_element else ""
            
            # Calculate the similarity score for the product name
            similarity_score = fuzz.token_sort_ratio(product, product_name)

            if similarity_score > max_similarity_score:
                # Update the maximum similarity score and the corresponding item
                max_similarity_score = similarity_score
                max_similarity_item = sibling_item

        except NoSuchElementException as e:
            # Skip to the next item if NoSuchElementException occurs
            logging.debug(
                f'NoSuchElementException: {e}, Website: {website["url"]}, Product: {product}'
            )
            print("Skipping the current item due to NoSuchElementException.")
            pass

        try:
            sibling_item = wait_and_get_element_by_xpath_relative(sibling_item, "./following-sibling::*")
        except NoSuchElementException:
            # Break the loop if there are no more sibling items
            print("No more sibling items found.")
            break

    if max_similarity_item and max_similarity_score > 50:
        # Get the product name and price based on the item with the maximum similarity score
        product_name_element = get_product_name_element(max_similarity_item, class_names_set1)

        if product_name_element is None:
            product_name_element = get_product_name_element(max_similarity_item, class_names_set2)

        product_name = product_name_element.text if product_name_element else "Name not found"
        price_element = get_price_element(max_similarity_item)
        price = price_element.text if price_element else "Price not found"
        
        logging.info(
            f"Found the best match with similarity score {max_similarity_score}: {product_name}"
        )
        return website["url"], product_name, price
    
    logging.info(f"No matching product found on {website['url']}")
    return website["url"], "No matching product found", "Price not found"
