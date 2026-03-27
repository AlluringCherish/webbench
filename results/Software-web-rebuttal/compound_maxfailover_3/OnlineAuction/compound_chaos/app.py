from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

def load_data(filename):
    filepath = os.path.join('data', filename)
    data = []
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = [part.strip() for part in line.split(',')]
                    data.append(parts)
    return data

@app.route('/')
def index():
    categories = load_data('categories.txt')
    items = load_data('items.txt')
    offers = load_data('offers.txt')
    return render_template('index.html', categories=categories, items=items, offers=offers)

@app.route('/add_offer', methods=['POST'])
def add_offer():
    item_id = request.form.get('item_id')
    user_name = request.form.get('user_name')
    offer_amount = request.form.get('offer_amount')

    if not item_id or not user_name or not offer_amount:
        return "Missing data", 400

    try:
        offer_value = float(offer_amount)
    except ValueError:
        return "Invalid offer amount", 400

    offers = load_data('offers.txt')
    current_offers = [float(offer[2]) for offer in offers if offer[0] == item_id]

    if current_offers and offer_value <= max(current_offers):
        return "Offer must be higher than existing offers", 400

    offers_file = os.path.join('data', 'offers.txt')
    with open(offers_file, 'a', encoding='utf-8') as file:
        file.write(f"{item_id},{user_name},{offer_amount}\n")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
