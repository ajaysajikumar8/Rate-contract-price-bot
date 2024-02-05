import os
import logging
import time
import random
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

def setup_logging(log_file_name):
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = os.path.join(logs_dir, log_file_name)
    logging.basicConfig(filename=log_file_path, level=logging.INFO)

def introduce_delay():
    delay = random.uniform(1, 3)  # Random delay between 1 to 3 seconds
    time.sleep(delay)

def wait_and_get_element(driver, locator):
    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(locator)
    )

def wait_and_get_element_text(driver, locator):
    element = wait_and_get_element(driver, locator)
    return element.text if element else 'Not found'

def wait_and_get_element_by_xpath_relative(parent, xpath):
    return parent.find_element(By.XPATH, xpath)

def wait_and_get_element_by_class_name_relative(parent, class_name):
    return parent.find_element(By.CLASS_NAME, class_name)

def wait_and_get_element_by_class_name(driver, class_name):
    return driver.find_element(By.CLASS_NAME, class_name)

def wait_and_get_element_by_xpath(driver, xpath):
    return driver.find_element(By.XPATH, xpath)
