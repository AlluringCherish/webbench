from flask import Flask, render_template, request, redirect, url_for, session
import os
import threading
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Files
BOOKS_FILE = 'books.txt'
REVIEWS_FILE = 'reviews.txt'
ORDERS_FILE = 'orders.txt'
BESTSELLERS_FILE = 'bestsellers.txt'

lock = threading.Lock()

# Helper functions to read/write files safely

def read_books():
    books = []
    if not os.path.exists(BOOKS_FILE):
        return books
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 5:
                continue
            books.append({'id': parts[0], 'title': parts[1], 'author': parts[2], 'price': float(parts[3]), 'stock': int(parts[4])})
    return books

def write_books(books):
    with lock:
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            for b in books:
                f.write(f"{b['id']},{b['title']},{b['author']},{b['price']},{b['stock']}\n")

def read_reviews():
    reviews = []
    if not os.path.exists(REVIEWS_FILE):
        return reviews
    with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',', 3)
            if len(parts) < 4:
                continue
            reviews.append({'book_id': parts[0], 'username': parts[1], 'rating': int(parts[2]), 'comment': parts[3]})
    return reviews

def write_reviews(reviews):
    with lock:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            for r in reviews:
                f.write(f"{r['book_id']},{r['username']},{r['rating']},{r['comment']}\n")

def read_orders():
    orders = []
    if not os.path.exists(ORDERS_FILE):
        return orders
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 5:
                continue
            orders.append({'order_id': parts[0], 'username': parts[1], 'book_id': parts[2], 'quantity': int(parts[3]), 'total_price': float(parts[4])})
    return orders

def write_orders(orders):
    with lock:
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            for o in orders:
                f.write(f"{o['order_id']},{o['username']},{o['book_id']},{o['quantity']},{o['total_price']}\n")

def read_bestsellers():
    bestsellers = []
    if not os.path.exists(BESTSELLERS_FILE):
        return bestsellers
    with open(BESTSELLERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 2:
                continue
            bestsellers.append({'book_id': parts[0], 'sales_count': int(parts[1])})
    return bestsellers

def write_bestsellers(bestsellers):
    with lock:
        with open(BESTSELLERS_FILE, 'w', encoding='utf-8') as f:
            for b in bestsellers:
                f.write(f"{b['book_id']},{b['sales_count']}\n")

# Helper

def get_book(book_id):
    books = read_books()
    for b in books:
        if b['id'] == book_id:
            return b
    return None

def update_stock(book_id, qty):
    books = read_books()
    changed = False
    for b in books:
        if b['id'] == book_id:
            if b['stock'] < qty:
                return False
            b['stock'] -= qty
            changed = True
            break
    if changed:
        write_books(books)
    return changed

def add_order(username, book_id, quantity, total_price):
    orders = read_orders()
    order_id = str(uuid.uuid4())
    orders.append({'order_id': order_id, 'username': username, 'book_id': book_id, 'quantity': quantity, 'total_price': total_price})
    write_orders(orders)
    bestsellers = read_bestsellers()
    for b in bestsellers:
        if b['book_id'] == book_id:
            b['sales_count'] += quantity
            write_bestsellers(bestsellers)
            break
    else:
        bestsellers.append({'book_id': book_id, 'sales_count': quantity})
        write_bestsellers(bestsellers)

@app.route('/')
def dashboard():
    books = read_books()
    bestsellers = read_bestsellers()
    bestsellers_sorted = sorted(bestsellers, key=lambda x: x['sales_count'], reverse=True)[:5]
    featured_books = [get_book(b['book_id']) for b in bestsellers_sorted if get_book(b['book_id'])]
    return render_template('dashboard.html', books=books, featured_books=featured_books)

@app.route('/book/<book_id>')
def book_detail(book_id):
    book = get_book(book_id)
    if not book:
        return "Not Found", 404
    reviews = [r for r in read_reviews() if r['book_id'] == book_id]
    return render_template('book_detail.html', book=book, reviews=reviews)

@app.route('/add_review/<book_id>', methods=['POST'])
def add_review(book_id):
    username = request.form.get('username')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    if not username or not rating or not comment:
        return redirect(url_for('book_detail', book_id=book_id))
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return redirect(url_for('book_detail', book_id=book_id))
    except:
        return redirect(url_for('book_detail', book_id=book_id))
    reviews = read_reviews()
    reviews.append({'book_id': book_id, 'username': username, 'rating': rating, 'comment': comment})
    write_reviews(reviews)
    return redirect(url_for('book_detail', book_id=book_id))

@app.route('/cart')
def view_cart():
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart_items = []
    total = 0.0
    for book_id, qty in cart.items():
        book = get_book(book_id)
        if book:
            subtotal = book['price'] * qty
            cart_items.append({'book': book, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', cart_items=cart_items, total_price=total)

@app.route('/add_to_cart/<book_id>', methods=['POST'])
def add_to_cart(book_id):
    qty = request.form.get('quantity', 1)
    try:
        qty = int(qty)
        if qty < 1:
            qty = 1
    except:
        qty = 1
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[book_id] = cart.get(book_id, 0) + qty
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    for key, val in request.form.items():
        try:
            qty = int(val)
            if qty > 0:
                cart[key] = qty
            else:
                cart.pop(key, None)
        except:
            pass
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    username = request.form.get('username')
    if not username:
        return redirect(url_for('view_cart'))
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('view_cart'))
    cart = session['cart']
    for book_id, qty in cart.items():
        book = get_book(book_id)
        if not book or book['stock'] < qty:
            return redirect(url_for('view_cart'))
    total_price = 0.0
    for book_id, qty in cart.items():
        book = get_book(book_id)
        if update_stock(book_id, qty):
            total_price += book['price'] * qty
            add_order(username, book_id, qty, book['price'] * qty)
        else:
            return redirect(url_for('view_cart'))
    session['cart'] = {}
    return render_template('checkout_success.html', username=username, total_price=total_price)

@app.route('/orders/<username>')
def view_orders(username):
    orders = [o for o in read_orders() if o['username'] == username]
    orders_detailed = []
    for o in orders:
        book = get_book(o['book_id'])
        if book:
            o_data = o.copy()
            o_data['book_title'] = book['title']
            orders_detailed.append(o_data)
    return render_template('orders.html', orders=orders_detailed, username=username)

if __name__ == '__main__':
    app.run(debug=True)
