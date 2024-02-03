# test_app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the product name from the form
        product_name = request.form.get('product_name')

        # Make an API request to the search_product route in your main application
        api_url = 'http://localhost:5000/search_product'

        #Structure of Input Data
        payload = {'product_name': product_name}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            # If the API request is successful, get the results
            results = response.json()
            return render_template('result.html', results=results)
        else:
            # If there's an error in the API request, handle it accordingly
            error_message = f"Error: {response.status_code} - {response.text}"
            return render_template('error.html', error_message=error_message)

    # If it's a GET request or before submitting the form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
