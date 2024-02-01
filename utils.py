# utils.py
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

def wait_and_get_element(driver, locator):
    return WebDriverWait(driver, 10).until(
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
