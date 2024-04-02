from flask import Flask, render_template, request, redirect, url_for
import get_products

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/<str>", methods=['GET', 'POST'])
def results_page(str):
    list = []
    get_products.amazon_products(str, list)
    get_products.flipkart_products(str, list)

    filtered_and_sorted_list = []

    if request.method == 'POST':
        min_rating = int(request.form.get('userRating'))
        min_price = int(request.form.get('minPrice'))
        max_price = int(request.form.get('maxPrice'))  # Retrieve user rating from the form
    else:
        # Default value if the form is not submitted
        min_rating = 4
        min_price = 0
        max_price = 1000
    

    for entry in list:
        entry['price'] = float(entry['price'].replace('₹', '').replace(',', ''))
        if (float(entry['rating']) >= min_rating) and (entry['price'] <= max_price) and (entry['price'] >= min_price):
            filtered_and_sorted_list.append(entry)

    sorted_list = sorted(filtered_and_sorted_list, key=lambda x: x['price'])
    return render_template('results.html', products=sorted_list)

@app.route("/search", methods=['GET', 'POST'])
def search_page():
    if request.method == "POST":
        search_query = request.form["nm"].replace(" ", "+")
        return redirect(url_for('results_page', str=search_query))
    else:
        return render_template('search.html')

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

