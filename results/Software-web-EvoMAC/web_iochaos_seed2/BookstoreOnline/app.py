'''
Flask backend for BookstoreOnline web application.
Provides route handlers for all pages and API endpoints,
manages data stored in local text files under 'data' directory.
'''
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
            book = {
                'book_id': parts[0],
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'category': parts[4],
                'price': float(parts[5]),
                'stock': int(parts[6]),
                'description': parts[7]
            }
            books.append(book)
    return books
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 3:
                continue
            category = {
                'category_id': parts[0],
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(category)
    return categories
def read_cart():
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if not os.path.exists(path):
        return cart_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 4:
                continue
            item = {
                'cart_id': parts[0],
                'book_id': parts[1],
                'quantity': int(parts[2]),
                'added_date': parts[3]
            }
            cart_items.append(item)
    return cart_items
def write_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart_items:
            line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)
def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            order = {
                'order_id': parts[0],
                'customer_name': parts[1],
                'order_date': parts[2],
                'total_amount': float(parts[3]),
                'status': parts[4],
                'shipping_address': parts[5]
            }
            orders.append(order)
    return orders
def read_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    if not os.path.exists(path):
        return order_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 5:
                continue
            item = {
                'order_item_id': parts[0],
                'order_id': parts[1],
                'book_id': parts[2],
                'quantity': int(parts[3]),
                'price': float(parts[4])
            }
            order_items.append(item)
    return order_items
def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            review = {
                'review_id': parts[0],
                'book_id': parts[1],
                'customer_name': parts[2],
                'rating': parts[3],
                'review_text': parts[4],
                'review_date': parts[5]
            }
            reviews.append(review)
    return reviews
def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(line)
def read_bestsellers():
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    if not os.path.exists(path):
        return bestsellers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 3:
                continue
            bestseller = {
                'book_id': parts[0],
                'sales_count': int(parts[1]),
                'period': parts[2]
            }
            bestsellers.append(bestseller)
    return bestsellers
@app.route('/')
def dashboard():
    books = read_books()
    # For featured books, pick first 3 books as example
    featured_books = books[:3] if len(books) >= 3 else books
    # Load bestsellers for "This Month" by default
    bestsellers_data = read_bestsellers()
    bestsellers_filtered = [b for b in bestsellers_data if b['period'] == 'This Month']
    # Rank bestsellers by sales_count descending
    bestsellers_sorted = sorted(bestsellers_filtered, key=lambda x: x['sales_count'], reverse=True)
    # Attach book info to bestsellers
    bestsellers = []
    rank = 1
    for b in bestsellers_sorted:
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        if book:
            bestsellers.append({
                'rank': rank,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
            rank += 1
    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)
@app.route('/catalog')
def catalog():
    books = read_books()
    categories = read_categories()
    # Add "All" option for category filter
    categories.insert(0, {'category_id': '0', 'category_name': 'All', 'description': 'All categories'})
    return render_template('catalog.html', books=books, categories=categories)
@app.route('/book/<book_id>')
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404
    reviews = read_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=book_reviews)
@app.route('/cart')
def cart():
    cart_items = read_cart()
    books = read_books()
    # Join cart items with book info
    items = []
    total_amount = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            subtotal = book['price'] * item['quantity']
            total_amount += subtotal
            items.append({
                'cart_id': item['cart_id'],
                'book_id': book['book_id'],
                'title': book['title'],
                'quantity': item['quantity'],
                'price': book['price'],
                'subtotal': subtotal
            })
    return render_template('cart.html', items=items, total_amount=total_amount)
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    book_id = data.get('book_id')
    if not book_id:
        return jsonify(success=False, message="Missing book_id"), 400
    cart_items = read_cart()
    # Check if book already in cart, increment quantity if so
    for item in cart_items:
        if item['book_id'] == book_id:
            item['quantity'] += 1
            write_cart(cart_items)
            return jsonify(success=True)
    # Else add new cart item with new cart_id
    new_id = 1
    if cart_items:
        new_id = max(int(i['cart_id']) for i in cart_items) + 1
    today = datetime.date.today().isoformat()
    cart_items.append({
        'cart_id': str(new_id),
        'book_id': book_id,
        'quantity': 1,
        'added_date': today
    })
    write_cart(cart_items)
    return jsonify(success=True)
@app.route('/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')
    if not cart_id or quantity is None:
        return jsonify(success=False, message="Missing cart_id or quantity"), 400
    try:
        quantity = int(quantity)
        if quantity < 1:
            return jsonify(success=False, message="Quantity must be at least 1"), 400
    except:
        return jsonify(success=False, message="Invalid quantity"), 400
    cart_items = read_cart()
    updated = False
    for item in cart_items:
        if item['cart_id'] == cart_id:
            item['quantity'] = quantity
            updated = True
            break
    if not updated:
        return jsonify(success=False, message="Cart item not found"), 404
    write_cart(cart_items)
    return jsonify(success=True)
@app.route('/cart/remove', methods=['POST'])
def remove_cart_item():
    data = request.get_json()
    cart_id = data.get('cart_id')
    if not cart_id:
        return jsonify(success=False, message="Missing cart_id"), 400
    cart_items = read_cart()
    new_cart = [item for item in cart_items if item['cart_id'] != cart_id]
    if len(new_cart) == len(cart_items):
        return jsonify(success=False, message="Cart item not found"), 404
    write_cart(new_cart)
    return jsonify(success=True)
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
@app.route('/orders')
def orders():
    orders = read_orders()
    return render_template('orders.html', orders=orders)
@app.route('/order/<order_id>')
def order_details(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    order_items = read_order_items()
    books = read_books()
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            book = next((b for b in books if b['book_id'] == oi['book_id']), None)
            if book:
                items.append({
                    'order_item_id': oi['order_item_id'],
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })
    return render_template('order_details.html', order=order, items=items)
@app.route('/reviews')
def reviews():
    reviews = read_reviews()
    books = read_books()
    # Attach book title to each review
    for r in reviews:
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        r['book_title'] = book['title'] if book else 'Unknown'
    return render_template('reviews.html', reviews=reviews)
@app.route('/reviews/submit', methods=['POST'])
def submit_review():
    data = request.get_json()
    book_id = data.get('book_id')
    rating = data.get('rating')
    review_text = data.get('review_text')
    if not book_id or not rating or not review_text:
        return jsonify(success=False, message="Missing fields"), 400
    reviews = read_reviews()
    new_id = 1
    if reviews:
        new_id = max(int(r['review_id']) for r in reviews) + 1
    today = datetime.date.today().isoformat()
    # Since no authentication, use 'Anonymous' as customer_name
    reviews.append({
        'review_id': str(new_id),
        'book_id': book_id,
        'customer_name': 'Anonymous',
        'rating': rating,
        'review_text': review_text,
        'review_date': today
    })
    write_reviews(reviews)
    return jsonify(success=True)
@app.route('/write_review')
def write_review():
    books = read_books()
    return render_template('write_review.html', books=books)
@app.route('/bestsellers')
def bestsellers():
    period = request.args.get('period', 'This Month')
    bestsellers_data = read_bestsellers()
    filtered = [b for b in bestsellers_data if b['period'] == period]
    books = read_books()
    bestsellers = []
    rank = 1
    for b in sorted(filtered, key=lambda x: x['sales_count'], reverse=True):
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        if book:
            bestsellers.append({
                'rank': rank,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
            rank += 1
    return render_template('bestsellers.html', bestsellers=bestsellers, period=period)
if __name__ == '__main__':
    app.run(debug=True)