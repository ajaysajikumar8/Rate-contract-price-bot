# main.py
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from websites import websites
from search_product import search_product
from find_similar_item import find_similar_item
import os
import logging

logging.basicConfig(filename='logs/main.log', level=logging.INFO)

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

app = Flask(__name__)

def scrape_website(driver, website_info, product_name):
    site, product, price = search_product(
        driver,
        website_info,
        product_name
    )
    return site, product, price

@app.route('/search_product', methods=['POST'])
def search_product_route():
    data = request.get_json()
    product_name = data.get('product_name')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Hey")
        results = []
        for website_info in websites:
            site, product, price = scrape_website(driver, website_info, product_name)
            print(site, product, price)
            result = {
                "website": site,
                "product": product,
                "price": price
            }
            results.append(result)
    finally:
        driver.quit()

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)
