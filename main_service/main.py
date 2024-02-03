# main.py
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from websites import websites
from search_product import search_product
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

def scrape_website(args_tuple):
    website_info, product_name = args_tuple
    with webdriver.Chrome(options=chrome_options) as driver:
        site, product, price = search_product(driver, website_info, product_name)
    return {'website': site, 'product': product, 'price': price}

def create_webdriver():
    return webdriver.Chrome(options=chrome_options)

def parallel_scrape(product_name):
    with ThreadPoolExecutor() as executor:
        scrape_args = ((website_info, product_name) for website_info in websites)
        results = executor.map(scrape_website, scrape_args)

    return list(results)

@app.route('/search_product', methods=['POST'])
def search_product_route():
    data = request.get_json()
    product_name = data.get('product_name')

    results = parallel_scrape(product_name)

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)
