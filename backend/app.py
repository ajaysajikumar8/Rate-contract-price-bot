from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from websites import websites
from search_product import search_product
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
import time
import os
import logging
import random
import requests

logging.basicConfig(filename="logs/main.log", level=logging.INFO)

ua = UserAgent()

def create_session():
    user_agent = ua.random
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": os.getenv("ACCEPT_LANGUAGE"),
        "Accept": os.getenv("ACCEPT"),
        "Accept-Encoding": os.getenv("ACCEPT_ENCODING"),
    }

    session = requests.Session()
    session.headers.update(headers)

    # Mount the session to retry on failures
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))

    return session

chrome_options = Options()
chrome_options.add_argument("--headless")
load_dotenv()

def create_webdriver(session):
    for key, value in session.headers.items():
        chrome_options.add_argument(f"--header={key}: {value}")

    delay = random.uniform(1, 3)
    time.sleep(delay)

    # Set cookies in the webdriver
    for cookie in session.cookies:
        chrome_options.add_argument(f"--cookie={cookie.name}={cookie.value}")

    return webdriver.Chrome(options=chrome_options)

app = Flask(__name__)

def scrape_website(args_tuple):
    website_info, product_name = args_tuple
    session = create_session()
    with create_webdriver(session) as driver:
        site, product, price = search_product(driver, website_info, product_name)
    return {"website": site, "product": product, "price": price}

def parallel_scrape(product_name):
    random.shuffle(websites)
    with ThreadPoolExecutor() as executor:
        scrape_args = ((website_info, product_name) for website_info in websites)
        results = executor.map(scrape_website, scrape_args)

    return list(results)

@app.route("/search_product", methods=["POST"])
def search_product_route():
    data = request.get_json()
    product_name = data.get("product_name")

    results = parallel_scrape(product_name)

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5000)
