from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')


# Utility functions to load data from files

def load_users():
    users = []
    try:
        with open(os.path.join(DATA_FOLDER, 'users.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    users.append({
                        'username': parts[0],
                        'password': parts[1],
                        'email': parts[2]
                    })
    except FileNotFoundError:
        pass
    return users


def load_categories():
    categories = []
    try:
        with open(os.path.join(DATA_FOLDER, 'categories.txt'), 'r') as f:
            for line in f:
                categories.append(line.strip())
    except FileNotFoundError:
        pass
    return categories


def load_auctions():
    auctions = []
    try:
        with open(os.path.join(DATA_FOLDER, 'auctions.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                # Assuming auctions.txt line format: id,product_name,category,starting_price,current_price,seller,bid_count
                if len(parts) == 7:
                    auctions.append({
                        'id': parts[0],
                        'product_name': parts[1],
                        'category': parts[2],
                        'starting_price': float(parts[3]),
                        'current_price': float(parts[4]),
                        'seller': parts[5],
                        'bid_count': int(parts[6])
                    })
    except FileNotFoundError:
        pass
    return auctions


@app.route('/')
def home():
    categories = load_categories()
    auctions = load_auctions()
    return render_template('home.html', categories=categories, auctions=auctions)


@app.route('/auctions')
def auctions():
    auctions = load_auctions()
    return jsonify(auctions)


@app.route('/users')
def users():
    users = load_users()
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
