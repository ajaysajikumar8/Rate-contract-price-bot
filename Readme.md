# Project Documentation: Product Price Fetcher

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
3. [Usage](#usage)
    - [Running the Script](#running-the-script)
    - [Input](#input)
    - [Output](#output)
4. [Project Structure](#project-structure)
5. [Modules and Components](#modules-and-components)
    - [1. main.py](#1-mainpy)
    - [2. search_product.py](#2-search_productpy)
    - [3. find_similar_item.py](#3-find_similar_itempy)
    - [4. utils.py](#4-utilspy)
    - [5. websites.py](#5-websitespy)
6. [Logging](#logging)
7. [Error Handling](#error-handling)
8. [Search Algorithm](#search-algorithm)
    - [Similarity Score Calculation](#similarity-score-calculation)
    - [Handling Similarity Score in Results](#handling-similarity-score-in-results)
9. [Parallel Scraping](#parallel-scraping)
10. [Future Enhancements](#future-enhancements)
11. [Conclusion](#conclusion)

---

## Introduction

The Product Price Fetcher is a Python script designed to retrieve and compare prices of a given product from various e-commerce websites. It utilizes Selenium for web scraping and provides a modular and extensible structure.

---

## Getting Started

### Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver executable

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/product-price-fetcher.git
    cd product-price-fetcher
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

### Running the Script

Execute the `main.py` script:

```bash
python main.py
```

### Input

The Product Price Fetcher requires input in the form of a JSON object containing the following key:

- `product_name`: The name of the product you are searching for.

Example Input:

```json
{
  "product_name": "Smartphone"
}
```

### Output

The script will display the prices for the specified product on different websites.


```json
[
  {
    "website": "https://www.example1.com",
    "product": "Smartphone Model X",
    "price": "$499.99"
  },
  {
    "website": "https://www.example2.com",
    "product": "Super Smartphone",
    "price": "$449.99"
  },
]
```

## Project Structure

The project follows a modular structure with the following main files:

1. **main.py**: Orchestrates the overall execution of the script.
2. **search_product.py**: Handles the search functionality on e-commerce websites.
3. **find_similar_item.py**: Finds the most similar item based on product names.
4. **utils.py**: Contains utility functions used across multiple modules.
5. **websites.py**: Stores information about various e-commerce websites, including URLs and locators.

---

## Modules and Components

### 1. main.py

- Initializes the Chrome WebDriver.
- Iterates over defined websites and calls `scrape_website` function.
- Prints product prices.

### 2. search_product.py

- Searches for the specified product on the given website.
- Uses `find_similar_item` to find the most similar item.

### 3. find_similar_item.py

- Finds the most similar item based on product names.
- Handles class name variations for different types of products.
- Logs errors and exceptions for debugging.

### 4. utils.py

- Provides utility functions like waiting for elements and retrieving element text.

### 5. websites.py

- Stores information about various e-commerce websites, including URLs and locators.

---

## Logging

The project uses the Python `logging` module to log information, warnings, errors, and debug messages. Log files are stored in the 'logs' directory.

---

## Error Handling

The script handles exceptions such as `NoSuchElementException` and `TimeoutException`. Detailed error logs are available in log files for debugging.

---

## Search Algorithm

### Similarity Score Calculation

The similarity score between the searched product and the retrieved product names is calculated using the FuzzyWuzzy library. This score helps determine the closeness of the match.

### Handling Similarity Score in Results

The project considers the similarity score when presenting search results. If the similarity score is above a certain threshold (e.g., 50%), the script considers it a potential match. This allows for flexibility, enabling the retrieval of products with varying levels of name similarity.

---

## Parallel Scraping

### Parallel Scraping Function (parallel_scrape)

A new function parallel_scrape was introduced to handle the parallel scraping of websites. It utilizes the ThreadPoolExecutor from the concurrent.futures module, which allows concurrent execution of functions using threads. The function takes the product name as an argument and uses a thread pool to execute the scrape_website function for each website concurrently.

### Concurrency and Performance

By using threads, the function achieves concurrency, allowing multiple websites to be scraped simultaneously. This is beneficial when dealing with I/O-bound tasks, such as web scraping, where the program often waits for external resources (like web pages to load). While one thread is waiting for a response from a website, other threads can continue working, leading to improved overall efficiency.

### Thread Safety

Each thread in the pool executes the scrape_website function independently with its own set of arguments. Thread safety is maintained by ensuring that shared resources (like the webdriver instance) are properly managed. In this case, the webdriver is created and used within the scrape_website function.

### Benefits

- Parallel processing reduces the time it takes to scrape information from multiple websites compared to sequential processing.
- It enhances the efficiency of the web scraping application, especially when dealing with a large number of websites.

---

## Future Enhancements

### 1. Handling CAPTCHA Verification

Address the challenge of CAPTCHA verification when encountered during scraping. Implement mechanisms to detect and handle CAPTCHAs gracefully. Potential solutions include using CAPTCHA solving services or incorporating CAPTCHA-solving libraries to automate the verification process.

### 2. Enhanced Exception Handling

Implement more advanced exception handling to gracefully manage various scenarios. Enhance the error reporting and recovery mechanisms to ensure robustness in the face of unexpected issues during web scraping. This will contribute to a more reliable and resilient application.

### 3. Scalability

Optimize the codebase for scalability to handle an increasing number of requests. Consider containerization technologies like Docker for easy deployment and scaling of the application.

### 4. Security Considerations

Introduce security measures to protect against potential vulnerabilities. When exposing the module as a service, implement authentication mechanisms, secure endpoints, and data encryption to ensure the confidentiality and integrity of the communication between the external applications and the module.

---

## Conclusion

The Product Price Fetcher provides a foundation for scraping product prices from different e-commerce websites. It is designed to be modular, extensible, and easily maintainable. Contributions and feedback are welcome.

---