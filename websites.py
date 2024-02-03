# websites.py
websites = [
    {
        'url': 'https://www.amazon.in',
        'search_bar_locator': ('xpath', '//*[@id="twotabsearchtextbox"]'),
        'first_item_locator': ('xpath', '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]'),
        'product_name_locator': [
            ('class_name', 'a-size-medium.a-color-base.a-text-normal'),
            ('class_name', 'a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4')
        ],
        'price_locator': ('class_name', 'a-price-whole'),
    },
    {
        'url': 'https://www.flipkart.com',
        'search_bar_locator': ('xpath', '//*[@id="container"]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div/div[1]/div[1]/header/div[1]/div[2]/form/div/div/input'),
        'first_item_locator': ('xpath', '//*[@id="container"]/div/div[3]/div/div[2]/div[2]'),
        'product_name_locator': [('class_name', '_4rR01T'), ('class_name', 's1Q9rs')],
        'price_locator': ('class_name', '_30jeq3'),
    }
    # Add more websites and their rules as needed
]
