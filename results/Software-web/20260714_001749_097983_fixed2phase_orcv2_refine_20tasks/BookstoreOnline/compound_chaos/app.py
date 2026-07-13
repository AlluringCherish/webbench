from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import json
import os
from threading import Lock

app = Flask(__name__)
app.secret_key = 'somesecretkey'

BOOKS_FILE = 'books.json'
BESTSELLERS_FILE = 'bestsellers.json'
REVIEWS_FILE = 'reviews.json'
ORDERS_FILE = 'orders.json'

lock = Lock()

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_books():
    return load_json(BOOKS_FILE)

def get_bestsellers():
    return load_json(BESTSELLERS_FILE)

def get_reviews():
    return load_json(REVIEWS_FILE)

def get_orders():
    return load_json(ORDERS_FILE)

def save_review(review):
    with lock:
        reviews = get_reviews()
        reviews.append(review)
        save_json(REVIEWS_FILE, reviews)

def save_order(order):
    with lock:
        orders = get_orders()
        orders.append(order)
        save_json(ORDERS_FILE, orders)

@app.route('/')
def dashboard():
    books = get_books()
    bestsellers = get_bestsellers()
    return render_template('dashboard.html', books=books, bestsellers=bestsellers)

@app.route('/book/<book_id>')
def book_details(book_id):
    books = get_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('dashboard'))
    book_reviews = [r for r in get_reviews() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=book_reviews)

@app.route('/cart')
def cart():
    cart_cookie = request.cookies.get('cart')
    cart = json.loads(cart_cookie) if cart_cookie else {}
    books = get_books()
    cart_items = []
    total = 0.0
    for book_id, qty in cart.items():
        book = next((b for b in books if b['id'] == book_id), None)
        if book:
            item_total = book['price'] * qty
            cart_items.append({**book, 'quantity': qty, 'total': item_total})
            total += item_total
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    book_id = request.form.get('book_id')
    quantity = int(request.form.get('quantity', 1))
    resp = make_response(redirect(url_for('cart')))
    cart_cookie = request.cookies.get('cart')
    cart = json.loads(cart_cookie) if cart_cookie else {}
    cart[book_id] = cart.get(book_id, 0) + quantity
    resp.set_cookie('cart', json.dumps(cart))
    flash('Added to cart.', 'success')
    return resp

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = {}
    books = get_books()
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            book_id = key[len('quantity_'):]
            try:
                qty = int(value)
                if qty > 0:
                    cart[book_id] = qty
            except ValueError:
                continue
    resp = make_response(redirect(url_for('cart')))
    resp.set_cookie('cart', json.dumps(cart))
    flash('Cart updated.', 'success')
    return resp

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_cookie = request.cookies.get('cart')
    if not cart_cookie:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('dashboard'))
    cart = json.loads(cart_cookie)
    books = get_books()
    cart_items = []
    total = 0.0
    for book_id, qty in cart.items():
        book = next((b for b in books if b['id'] == book_id), None)
        if book:
            item_total = book['price'] * qty
            cart_items.append({**book, 'quantity': qty, 'total': item_total})
            total += item_total

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        email = request.form.get('email')
        if not name or not address or not email:
            flash('Please fill in all fields.', 'error')
            return render_template('checkout.html', cart_items=cart_items, total=total)
        order = {
            'name': name,
            'address': address,
            'email': email,
            'items': cart_items
        }
        save_order(order)
        resp = make_response(redirect(url_for('order_confirmation')))
        resp.set_cookie('cart', '', expires=0)
        flash('Order placed successfully!', 'success')
        return resp

    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

@app.route('/order_history')
def order_history():
    orders = get_orders()
    return render_template('order_history.html', orders=orders)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    book_id = request.form.get('book_id')
    rating_str = request.form.get('rating', '0')
    comment = request.form.get('comment', '').strip()
    try:
        rating = int(rating_str)
    except ValueError:
        rating = 0
    if not book_id or rating < 1 or rating > 5 or not comment:
        flash('Invalid review submission.', 'error')
        return redirect(url_for('dashboard'))
    review = {
        'book_id': book_id,
        'rating': rating,
        'comment': comment
    }
    save_review(review)
    flash('Review submitted. Thank you!', 'success')
    return redirect(url_for('book_details', book_id=book_id))

if __name__ == '__main__':
    app.run(debug=True)
