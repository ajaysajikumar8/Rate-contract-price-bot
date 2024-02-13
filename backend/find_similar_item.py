from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from utils import (
    wait_and_get_element_by_class_name_relative,
    wait_and_get_element_by_xpath_relative,
    setup_logging,
)
import logging
from fuzzywuzzy import fuzz
import time

setup_logging("find_similar_item.log")


def find_similar_item(website, product, first_item):
    max_similarity_score = 0
    max_similarity_item = None
    sibling_item = first_item

    # List of sets of class names
    class_names_sets = [
        website_info[1] for website_info in website["product_name_locator"]
    ]

    def get_product_name_element(sibling_item, class_names):
        try:
            return wait_and_get_element_by_class_name_relative(
                sibling_item, class_names
            )
        except NoSuchElementException as e:
            logging.debug(
                f'NoSuchElementException: {e}, Website: {website["url"]}, Product: {product}'
            )
            return None

    def get_price_element(item):
        try:
            return wait_and_get_element_by_class_name_relative(
                item, website["price_locator"][1]
            )
        except NoSuchElementException as e:
            return None

    def extract_product_name(product_name_element):
        if (
            website["url"] == "https://www.flipkart.com"
            and product_name_element.get_attribute("class") != "_4rR01T"
        ):
            return product_name_element.get_attribute("title")
        else:
            return product_name_element.text

    for _ in range(10):  # Fetch product names for the first 6 items
        # Iterate through each set of class names
        for class_names_set in class_names_sets:
            try:
                product_name_element = get_product_name_element(
                    sibling_item, class_names_set
                )

                if product_name_element:
                    product_name = extract_product_name(product_name_element)
                    # Calculate the similarity score for the product name
                    similarity_score = fuzz.token_sort_ratio(product, product_name)

                    if similarity_score > max_similarity_score:
                        # Update the maximum similarity score and the corresponding item
                        max_similarity_score = similarity_score
                        max_similarity_item = sibling_item

            except NoSuchElementException as e:
                # Log the exception and move on to the next set of class names
                logging.info(
                    f'NoSuchElementException: {e}, Website: {website["url"]}, Product: {product}'
                )
                continue
        try:
            sibling_item = wait_and_get_element_by_xpath_relative(
                sibling_item, "./following-sibling::*"
            )
        except NoSuchElementException:
            # Break the loop if there are no more sibling items
            logging.info("No more siblings found")
            break

    if max_similarity_item and max_similarity_score > 30:
        # Get the product name and price based on the item with the maximum similarity score
        for class_names_set in class_names_sets:
            try:
                product_name_element = get_product_name_element(
                    max_similarity_item, class_names_set
                )

                if product_name_element:
                    product_name = extract_product_name(product_name_element)
                    price_element = get_price_element(max_similarity_item)
                    price = price_element.text if price_element else "Price not found"
                    if "₹" not in price:
                        price = "₹" + price

                    logging.info(
                        f"Found the best match with similarity score {max_similarity_score}: {product_name} on {website['url']}"
                    )
                    return website["url"], product_name, price

            except NoSuchElementException as e:
                # Log the exception and move on to the next set of class names
                logging.debug(
                    f'NoSuchElementException: {e}, Website: {website["url"]}, Product: {product}'
                )
                continue

    logging.info(f"No matching product found on {website['url']}")
    return website["url"], "No matching product found", "Price not found"
